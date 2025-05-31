import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from typing import Optional, Dict, Any
from data_types import RealEstateListing
import os
from PIL import Image
import math
from io import BytesIO

BASE_URL = "https://www.otodom.pl"
CITY = "krakow"
SEARCH_URL = f"{BASE_URL}/pl/wyniki/sprzedaz/mieszkanie/malopolskie/{CITY}/{CITY}/{CITY}?viewType=listing&page="
print(SEARCH_URL)


def sanitize_filename(filename):
    # usuń wszystko co nie jest literą, cyfrą, myślnikiem, podkreśleniem lub kropką
    return re.sub(r'[^a-zA-Z0-9_\-\.]', '_', filename)


def download_image_to_memory(url: str) -> Optional[Image.Image]:
    """Pobierz obraz do pamięci i zwróć obiekt PIL.Image"""
    print(f"Pobieram zdjęcie do pamięci: {url}")
    try:
        response = requests.get(url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        print(f"Błąd pobierania lub otwierania obrazu {url}: {e}")
        return None


def create_collage(images: list[Image.Image], collage_path: str, images_per_row=3):
    if not images:
        return

    # rozmiar pojedynczego obrazka
    img_width, img_height = images[0].size
    n_images = len(images)

    # obliczamy liczbę rzędów
    rows = math.ceil(n_images / images_per_row)

    # rozmiar końcowego kolażu
    collage_width = images_per_row * img_width
    collage_height = rows * img_height

    collage = Image.new("RGB", (collage_width, collage_height))

    for idx, img in enumerate(images):
        x = (idx % images_per_row) * img_width
        y = (idx // images_per_row) * img_height
        collage.paste(img, (x, y))

    collage.save(collage_path)
    print(f"Kolaż zapisany jako: {collage_path}")


def _extract_json_from_script(
    soup: BeautifulSoup, script_id: str = "__NEXT_DATA__"
) -> Optional[Dict]:
    try:
        script_tag = soup.find("script", {"id": script_id})
        if not script_tag or not script_tag.string:
            return None
        return json.loads(script_tag.string)
    except (json.JSONDecodeError, AttributeError) as e:
        print(f"Error extracting JSON from script tag: {str(e)}")
        return None


def _extract_ad_data(soup: BeautifulSoup) -> Optional[Dict]:
    json_data = _extract_json_from_script(soup)
    if not json_data:
        return None
    return json_data.get("props", {}).get("pageProps", {}).get("ad", {})


def _load_page(url: str) -> BeautifulSoup:
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_links_for_search_page(n: int) -> list[str]:
    url = SEARCH_URL + str(n)
    soup = _load_page(url)
    json_data = _extract_json_from_script(soup)

    if json_data:
        try:
            listings = json_data["props"]["pageProps"]["data"]["searchAds"]["items"]
            return [f"{BASE_URL}/pl/oferta/{listing['slug']}" for listing in listings]
        except KeyError as e:
            print(f"Error accessing listing data: {str(e)}")
    return []


def extract_data(
    url: str, soup: BeautifulSoup, debug: bool = False
) -> RealEstateListing:
    try:
        ad_data = _extract_ad_data(soup)
        if not ad_data:
            print(f"Warning: Could not extract ad data from {url}")
            return RealEstateListing.create_empty(url)

        photos = []
        images = ad_data.get("images", [])

        print(f"Liczba zdjęć: {len(images)}")
        for i, img in enumerate(images):
            print(f"Zdjęcie {i}: {img}")

        for img in images:
            photo_url = img.get("thumbnail") or img.get("small") or img.get("medium") or img.get("large")
            if photo_url:
                photos.append(photo_url)

        # Utwórz folder na kolaże wg slug z URL
        slug = url.split("/")[-1]
        folder = os.path.join("otodom_photos", slug)
        if not os.path.exists(folder):
            os.makedirs(folder)

        pil_images = []
        for photo_url in photos:
            img = download_image_to_memory(photo_url)
            if img:
                pil_images.append(img)

        collage_path = os.path.join(folder, f"{slug}_collage.jpg")

        if pil_images:
            create_collage(pil_images, collage_path)
            collage_file = collage_path
        else:
            collage_file = None

        location = (
            ad_data.get("location", {})
            .get("reverseGeocoding", {})
            .get("locations", {})[-1]
            .get("fullNameItems", [])
        )
        location_lat = ad_data.get("location", {}).get("coordinates", {}).get("latitude", None)
        location_lon = ad_data.get("location", {}).get("coordinates", {}).get("longitude", None)

        rooms_num = ad_data.get("target", {}).get("Rooms_num", [0])[0]

        return RealEstateListing(
            slug=slug,
            url=url,
            name=ad_data.get("title", None),
            price=ad_data.get("target", {}).get("Price", None),
            area=ad_data.get("target", {}).get("Area", None),
            rooms=rooms_num,
            build_year=ad_data.get("target", {}).get("Build_year", None),
            utilities=ad_data.get("features", []),
            location=location,
            location_lat=location_lat,
            location_lon=location_lon,
            heating=ad_data.get("target", {}).get("Heating", [None])[0],
            floor=ad_data.get("target", {}).get("Floor_no", [None])[0],
            building_floors=ad_data.get("target", {}).get("Building_floors_num", None),
            state=ad_data.get("target", {}).get("Construction_status", [None])[0],
            market=ad_data.get("target", {}).get("MarketType", None),
            ownership=ad_data.get("target", {}).get("Building_ownership", [None])[0],
            ad_type=ad_data.get("advertiserType", "brak informacji"),
            photos=[],  # Nie zapisujemy pojedynczych zdjęć na dysk ani ścieżek
            collage=collage_file,
        )

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        return RealEstateListing.create_empty(url)


def get_one_search_page(
    n: int, df_prev: pd.DataFrame, debug: bool = False
) -> pd.DataFrame:
    links = get_links_for_search_page(n)
    data_list = []
    for link in links:
        link = re.sub(r"ID\.", r"ID", link)
        if (not df_prev.empty) and (link in df_prev["url"].values):
            continue
        if (len(data_list)) and (link in [data.url for data in data_list]):
            continue

        print(f"Checking {link}")
        try:
            soup = _load_page(link)
            data = extract_data(link, soup, debug=debug)
            data_list.append(data)
        except Exception as e:
            print(f"Failed to process {link}: {str(e)}")
            continue

    if not data_list:
        return pd.DataFrame()

    df = pd.DataFrame(data_list)
    df.set_index("slug", inplace=True)
    return df


def get_n_pages(
    n: int, df_prev: pd.DataFrame, offset: int = 0, debug: bool = False
) -> pd.DataFrame:
    df = df_prev
    for i in range(offset, offset + n):
        print(f"\nProcessing page {i} of {offset + n -1}")
        page_df = get_one_search_page(i, df_prev, debug=debug)
        if df.empty:
            df = page_df
        elif not page_df.empty:
            page_df = page_df.dropna(axis=1, how="all")
            df = pd.concat([df, page_df], ignore_index=False)
        else:
            print(f"No (new) data found on page {i}")
    return df
