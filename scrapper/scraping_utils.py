import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
from typing import Optional, Dict, Any
from scrapper.data_types import RealEstateListing

BASE_URL = "https://www.otodom.pl"
CITY = "krakow"
SEARCH_URL = f"{BASE_URL}/pl/wyniki/sprzedaz/mieszkanie/malopolskie/{CITY}/{CITY}/{CITY}?viewType=listing&page="


def _extract_json_from_script(
    soup: BeautifulSoup, script_id: str = "__NEXT_DATA__"
) -> Optional[Dict]:
    """Extract JSON data from a script tag.

    Args:
        soup: BeautifulSoup object containing the page content
        script_id: ID of the script tag containing JSON data

    Returns:
        Parsed JSON data as a dictionary or None if extraction fails
    """
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


def _save_ad_data_to_file(url: str, ad_data: dict) -> None:
    """Save ad data as formatted JSON for analysis purposes.

    Args:
        url: The listing URL to use for the filename
        ad_data: The ad data dictionary to save
    """
    try:
        from pathlib import Path

        # Create logs directory if it doesn't exist
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)

        # Create filename using URL slug
        slug = url.split("/")[-1]
        log_file = log_dir / f"{slug}_ad_data.json"

        # Write formatted JSON
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(ad_data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving ad_data to file: {str(e)}")


def _load_page(url: str) -> BeautifulSoup:
    """Load and parse a webpage."""
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def _extract_number(text: str) -> Optional[float]:
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


def get_links_for_search_page(n: int) -> list[str]:
    """Get all listing links from a search results page."""
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
    """Extract data from a listing page and return a RealEstateListing instance"""
    try:
        ad_data = _extract_ad_data(soup)
        if not ad_data:
            print(f"Warning: Could not extract ad data from {url}")
            return RealEstateListing.create_empty(url)

        # Save the ad data if in debug mode
        if debug:
            _save_ad_data_to_file(url, ad_data)

        if not ad_data:
            print(f"Warning: Could not find ad data in JSON for {url}")
            return RealEstateListing.create_empty(url)

        location = (
            ad_data.get("location", {})
            .get("reverseGeocoding", {})
            .get("locations", {})[-1]
            .get("fullNameItems", [])
        )
        location_lat = (
            ad_data.get("location", {}).get("coordinates", {}).get("latitude", None)
        )
        location_lon = (
            ad_data.get("location", {}).get("coordinates", {}).get("longitude", None)
        )

        available = None
        extra_info = ad_data.get("additionalInformation", None)
        if extra_info:
            for item in extra_info:
                if item.get("label") == "free_from":
                    values = item.get("values", [None])
                    if values:
                        available = values[0]

        return RealEstateListing(
            slug=url.split("/")[-1],
            url=url,
            name=ad_data.get("title", None),
            price=ad_data.get("target", {}).get("Price", None),
            area=ad_data.get("target", {}).get("Area", None),
            rooms=ad_data.get("target", {}).get("Rooms_num", {})[0],
            build_year=ad_data.get("target", {}).get("Build_year", None),
            utilities=ad_data.get("features", []),
            location=location,
            location_lat=location_lat,
            location_lon=location_lon,
            heating=ad_data.get("target", {}).get("Heating", [None])[0],
            floor=ad_data.get("target", {}).get("Floor_no", [None])[0],
            building_floors=ad_data.get("target", {}).get("Building_floors_num", None),
            rent=ad_data.get("target", {}).get("Rent", None),
            state=ad_data.get("target", {}).get("Construction_status", [None])[0],
            market=ad_data.get("target", {}).get("MarketType", None),
            ownership=ad_data.get("target", {}).get("Building_ownership", [None])[0],
            available=available,
            ad_type=ad_data.get("advertiserType", "brak informacji"),
            extra_info="todo",
        )

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        import traceback

        print("Traceback:", traceback.format_exc())
        return RealEstateListing.create_empty(url)


def get_one_search_page(n: int, debug: bool = False) -> pd.DataFrame:
    """Get all listings from a single search page and return them as a DataFrame."""
    links = get_links_for_search_page(n)
    data_list = []
    for link in links:
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


def get_n_pages(n: int, offset: int = 0, debug: bool = False) -> pd.DataFrame:
    """Get listings from multiple pages and combine them into a single DataFrame."""
    df = pd.DataFrame()
    for i in range(offset, offset + n):
        print(f"\nProcessing page {i + 1} of {offset + n}")
        page_df = get_one_search_page(i, debug=debug)
        if not page_df.empty:
            df = pd.concat([df, page_df], ignore_index=False)
        else:
            print(f"No data found on page {i + 1}")
    return df
