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


def extract_json_from_script(
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
    json_data = extract_json_from_script(soup)

    if json_data:
        try:
            listings = json_data["props"]["pageProps"]["data"]["searchAds"]["items"]
            return [f"{BASE_URL}/pl/oferta/{listing['slug']}" for listing in listings]
        except KeyError as e:
            print(f"Error accessing listing data: {str(e)}")
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


def save_ad_data_to_file(url: str, ad_data: dict) -> None:
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


def extract_data(
    url: str, soup: BeautifulSoup, debug: bool = False
) -> RealEstateListing:
    """Extract data from a listing page and return a RealEstateListing instance"""
    try:
        json_data = extract_json_from_script(soup)
        if not json_data:
            print(f"Warning: Could not extract JSON data from {url}")
            return RealEstateListing.create_empty(url)

        ad_data = json_data.get("props", {}).get("pageProps", {}).get("ad", {})

        # Save the ad data if in debug mode
        if debug:
            save_ad_data_to_file(url, ad_data)

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
        location = []
        location_lat = None
        location_lon = None

        # Extract basic information
        name = ad_data.get("title", "brak informacji")

        # Extract location from map link
        map_link = soup.find("a", href="#map")
        if map_link:
            # Get only the text content, ignoring SVG and other elements
            location_text = "".join(text for text in map_link.stripped_strings)
            if location_text:
                # Split by comma and strip whitespace
                location = [part.strip() for part in location_text.split(",")]

        # Extract location coordinates
        location_data = ad_data.get("location", {})
        coordinates = location_data.get("coordinates", {})
        if coordinates:
            try:
                location_lat = float(coordinates.get("latitude"))
                location_lon = float(coordinates.get("longitude"))
            except (ValueError, TypeError):
                location_lat = None
                location_lon = None

        # Extract data from target
        target = ad_data.get("target", {})
        if target:
            # Extract price
            if "Price" in target:
                try:
                    price = float(target["Price"])
                except (ValueError, TypeError):
                    # Fallback to aria-label method
                    price_element = soup.find(attrs={"aria-label": "Cena"})
                    if price_element:
                        price = extract_number(price_element.text)

            # Extract area
            if "Area" in target:
                try:
                    area = float(target["Area"])
                except (ValueError, TypeError):
                    area = None

            # Extract rooms
            if "Rooms_num" in target and target["Rooms_num"]:
                try:
                    rooms = target["Rooms_num"][0]
                except (IndexError, TypeError):
                    rooms = "brak informacji"

            # Extract build year
            if "Build_year" in target:
                try:
                    build_year = int(target["Build_year"])
                except (ValueError, TypeError):
                    build_year = None

            # Extract elevator information
            if "Extras_types" in target:
                extras = target.get("Extras_types", [])
                elevator = "lift" in extras

            # Extract floor
            if "Floor_no" in target and target["Floor_no"]:
                try:
                    floor = target["Floor_no"][0]
                except (IndexError, TypeError):
                    floor = "brak informacji"

            # Extract other information
            market = target.get("Market", market)
            heating = target.get("Heating", heating)
            state = target.get("Construction_status", state)

        # Additional characteristics from characteristics array
        characteristics = ad_data.get("characteristics", [])
        for char in characteristics:
            if isinstance(char, dict):
                key = str(char.get("key", "")).lower()
                value = char.get("value")

                if "czynsz" in key:
                    rent = extract_number(str(value))
                elif "forma własności" in key:
                    ownership = value

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

        features_without_category = ad_data.get("featuresWithoutCategory", [])
        features.extend(
            [
                f.get("label", "")
                for f in features_without_category
                if isinstance(f, dict)
            ]
        )

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
            location=location,
            location_lat=location_lat,
            location_lon=location_lon,
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


def get_one_search_page(n: int, debug: bool = False) -> pd.DataFrame:
    """Get all listings from a single search page and return them as a DataFrame."""
    links = get_links_for_search_page(n)
    data_list = []
    for link in links:
        print(f"Checking {link}")
        try:
            soup = load_page(link)
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
