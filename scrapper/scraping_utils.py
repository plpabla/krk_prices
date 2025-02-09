import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from typing import Optional, Dict, Any
from scrapper.data_types import RealEstateListing

BASE_URL = "https://www.otodom.pl"
SEARCH_URL = (
    BASE_URL
    + "/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/krakow?viewType=listing&page="
)


def load_page(url: str) -> BeautifulSoup:
    """Load and parse a webpage."""
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_links_for_search_page(n: int) -> list[str]:
    """Get all listing links from a search results page."""
    url = SEARCH_URL + str(n)
    soup = load_page(url)
    script_tag = soup.find("script", {"id": "__NEXT_DATA__"})

    if script_tag:
        import json

        json_data = json.loads(script_tag.string)
        listings = json_data["props"]["pageProps"]["data"]["searchAds"]["items"]
        links = [f"{BASE_URL}/pl/oferta/{listing['slug']}" for listing in listings]
        return links
    return []


def safe_extract(
    soup: BeautifulSoup,
    selector: dict,
    attribute: Optional[str] = None,
    default: str = "brak informacji",
) -> str:
    """Safely extract data from BeautifulSoup object with fallbacks"""
    try:
        element = soup.find(**selector)
        if element is None:
            return default
        if attribute:
            return element.get(attribute, default)
        return element.text.strip()
    except Exception as e:
        print(f"Error extracting with selector {selector}: {str(e)}")
        return default


def extract_number(text: str) -> Optional[float]:
    """Extract number from text, handling various formats"""
    try:
        # Remove currency symbols, spaces, and convert commas to dots
        cleaned = re.sub(r"[^\d,.]", "", text.replace(",", "."))
        # Handle cases with multiple dots (take the last one as decimal separator)
        parts = cleaned.split(".")
        if len(parts) > 2:
            cleaned = "".join(parts[:-1]) + "." + parts[-1]
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


def find_info_row(soup: BeautifulSoup, label: str) -> str:
    """Find information row by label text"""
    try:
        elements = soup.find_all(["div", "span", "p"])
        for element in elements:
            if label.lower() in element.text.strip().lower():
                # Try to find the value in the next sibling or parent's next sibling
                next_element = element.find_next_sibling()
                if next_element:
                    return next_element.text.strip()
                parent_next = element.parent.find_next_sibling()
                if parent_next:
                    return parent_next.text.strip()
                # If no siblings found, return the parent's text excluding the label
                parent_text = element.parent.text.strip()
                return parent_text.replace(label, "").strip()
    except Exception as e:
        print(f"Error finding info row for {label}: {str(e)}")
    return "brak informacji"


def extract_data(url: str, soup: BeautifulSoup) -> RealEstateListing:
    """Extract data from a listing page and return a RealEstateListing instance"""
    try:
        # Extract JSON data from script tag
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag:
            import json

            json_data = json.loads(script_tag.string)
            ad_data = json_data.get("props", {}).get("pageProps", {}).get("ad", {})

            if not ad_data:
                print(f"Warning: Could not find ad data in JSON for {url}")
                return RealEstateListing.create_empty(url)

            # Initialize data with default values
            price = None
            area = None
            rooms = "brak informacji"
            heating = "brak informacji"
            floor = "brak informacji"
            rent = None
            state = "brak informacji"
            market = "brak informacji"
            ownership = "brak informacji"
            build_year = None
            elevator = False

            # Extract basic information
            name = ad_data.get("title", "brak informacji")

            # Price extraction from topInformation
            top_info = ad_data.get("topInformation", [])
            for info in top_info:
                if isinstance(info, dict):
                    label = str(info.get("label", "")).lower()
                    if "cena" in label or "price" in label:
                        price = extract_number(str(info.get("value", 0)))
                        break

            # Area and rooms extraction from topInformation
            for info in top_info:
                if isinstance(info, dict):
                    label = str(info.get("label", "")).lower()
                    value = info.get("value", "")

                    if "powierzchnia" in label:
                        area = extract_number(str(value))
                    elif "pokoje" in label:
                        rooms = value

            # Extract characteristics from target
            target = ad_data.get("target", {})
            if target:
                rooms = target.get("Rooms_num", rooms)
                market = target.get("Market", market)
                heating = target.get("Heating", heating)
                floor = target.get("Floor_no", floor)
                state = target.get("Construction_status", state)
                # Try to get build year from target data
                if "Build_year" in target:
                    try:
                        build_year = int(target["Build_year"])
                    except (ValueError, TypeError):
                        build_year = None

            # Additional characteristics from characteristics array
            characteristics = ad_data.get("characteristics", [])
            for char in characteristics:
                if isinstance(char, dict):
                    key = str(char.get("key", "")).lower()
                    value = char.get("value")

                    if "powierzchnia" in key and not area:
                        area = extract_number(str(value))
                    elif (
                        "liczba pokoi" in key or "pokoje" in key
                    ) and rooms == "brak informacji":
                        rooms = value
                    elif "ogrzewanie" in key and heating == "brak informacji":
                        heating = value
                    elif "piętro" in key and floor == "brak informacji":
                        floor = value
                    elif "czynsz" in key:
                        rent = extract_number(str(value))
                    elif "stan wykończenia" in key and state == "brak informacji":
                        state = value
                    elif "rynek" in key and market == "brak informacji":
                        market = value
                    elif "forma własności" in key:
                        ownership = value
                    elif "rok budowy" in key and not build_year:
                        try:
                            build_year = int(str(value))
                        except (ValueError, TypeError):
                            build_year = None

            # Extract features and additional information
            features = []
            features_by_category = ad_data.get("featuresByCategory", [])
            for category in features_by_category:
                if isinstance(category, dict):
                    category_features = category.get("features", [])
                    features.extend(
                        [
                            f.get("label", "")
                            for f in category_features
                            if isinstance(f, dict)
                        ]
                    )
                    # Check for elevator in features
                    for feature in category_features:
                        if (
                            isinstance(feature, dict)
                            and "winda" in str(feature.get("label", "")).lower()
                        ):
                            elevator = True
                            break

            features_without_category = ad_data.get("featuresWithoutCategory", [])
            features.extend(
                [
                    f.get("label", "")
                    for f in features_without_category
                    if isinstance(f, dict)
                ]
            )
            # Check for elevator in uncategorized features
            for feature in features_without_category:
                if (
                    isinstance(feature, dict)
                    and "winda" in str(feature.get("label", "")).lower()
                ):
                    elevator = True
                    break

            additional_info = ad_data.get("additionalInformation", [])
            features.extend(
                [
                    info.get("value", "")
                    for info in additional_info
                    if isinstance(info, dict)
                ]
            )

            extra_info = ", ".join(filter(None, features)) or "brak informacji"

            return RealEstateListing(
                slug=url.split("/")[-1],
                url=url,
                name=name,
                price=price,
                area=area,
                rooms=rooms,
                build_year=build_year,
                elevator=elevator,
                heating=heating,
                floor=floor,
                rent=rent,
                state=state,
                market=market,
                ownership=ownership,
                available="brak informacji",  # This field might not be available anymore
                ad_type=ad_data.get("advertiserType", "brak informacji"),
                extra_info=extra_info,
            )

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        import traceback

        print("Traceback:", traceback.format_exc())
        return RealEstateListing.create_empty(url)


def get_one_search_page(n: int) -> pd.DataFrame:
    """Get all listings from a single search page and return them as a DataFrame."""
    links = get_links_for_search_page(n)
    data_list = []
    for link in links:
        print(f"Checking {link}")
        try:
            soup = load_page(link)
            data = extract_data(link, soup)
            data_list.append(data)
        except Exception as e:
            print(f"Failed to process {link}: {str(e)}")
            continue

    if not data_list:
        return pd.DataFrame()

    df = pd.DataFrame(data_list)
    df.set_index("slug", inplace=True)
    return df


def get_n_pages(n: int, offset: int = 0) -> pd.DataFrame:
    """Get listings from multiple pages and combine them into a single DataFrame."""
    df = pd.DataFrame()
    for i in range(offset, offset + n):
        print(f"\nProcessing page {i + 1} of {offset + n}")
        page_df = get_one_search_page(i)
        if not page_df.empty:
            df = pd.concat([df, page_df], ignore_index=False)
        else:
            print(f"No data found on page {i + 1}")
    return df
