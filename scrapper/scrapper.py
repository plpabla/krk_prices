import requests
from bs4 import BeautifulSoup
import pandas as pd
import argparse
import re
from typing import Optional, Dict, Any

BASE_URL = "https://www.otodom.pl"
SEARCH_URL = (
    BASE_URL
    + "/pl/wyniki/sprzedaz/mieszkanie/malopolskie/krakow/krakow/krakow?viewType=listing&page="
)


def load_page(url: str) -> BeautifulSoup:
    res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser")
    return soup


def get_links_for_search_page(n: int) -> list[str]:
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


def extract_data(url: str, soup: BeautifulSoup) -> Dict[str, Any]:
    """Extract data from a listing page with improved error handling"""
    data = {"slug": url.split("/")[-1], "url": url}

    try:
        # Extract JSON data from script tag
        script_tag = soup.find("script", {"id": "__NEXT_DATA__"})
        if script_tag:
            import json

            json_data = json.loads(script_tag.string)

            # Get ad data
            ad_data = json_data.get("props", {}).get("pageProps", {}).get("ad", {})
            if not ad_data:
                print(f"Warning: Could not find ad data in JSON for {url}")
                return data

            # Extract basic information
            data["name"] = ad_data.get("title", "brak informacji")

            # Price extraction from topInformation
            top_info = ad_data.get("topInformation", [])
            for info in top_info:
                if isinstance(info, dict):
                    label = str(info.get("label", "")).lower()
                    if "cena" in label or "price" in label:
                        data["price"] = extract_number(str(info.get("value", 0)))
                        break

            # Area and rooms extraction from topInformation
            for info in top_info:
                if isinstance(info, dict):
                    label = str(info.get("label", "")).lower()
                    value = info.get("value", "")

                    if "powierzchnia" in label:
                        data["area"] = extract_number(str(value))
                    elif "pokoje" in label:
                        data["rooms"] = value

            # Extract characteristics from target
            target = ad_data.get("target", {})
            if target:
                data["rooms"] = target.get(
                    "Rooms_num", data.get("rooms", "brak informacji")
                )
                data["market"] = target.get("Market", "brak informacji")
                data["heating"] = target.get("Heating", "brak informacji")
                data["floor"] = target.get("Floor_no", "brak informacji")
                data["state"] = target.get("Construction_status", "brak informacji")

            # Additional characteristics from characteristics array
            characteristics = ad_data.get("characteristics", [])
            for char in characteristics:
                if isinstance(char, dict):
                    key = str(char.get("key", "")).lower()
                    value = char.get("value")

                    if "powierzchnia" in key and not data.get("area"):
                        data["area"] = extract_number(str(value))
                    elif ("liczba pokoi" in key or "pokoje" in key) and not data.get(
                        "rooms"
                    ):
                        data["rooms"] = value
                    elif "ogrzewanie" in key and data["heating"] == "brak informacji":
                        data["heating"] = value
                    elif "piętro" in key and data["floor"] == "brak informacji":
                        data["floor"] = value
                    elif "czynsz" in key:
                        data["rent"] = extract_number(str(value))
                    elif (
                        "stan wykończenia" in key and data["state"] == "brak informacji"
                    ):
                        data["state"] = value
                    elif "rynek" in key and data["market"] == "brak informacji":
                        data["market"] = value
                    elif "forma własności" in key:
                        data["ownership"] = value

            # Set defaults for unset values
            if "area" not in data or not data["area"]:
                data["area"] = 0.0
            if "price" not in data or not data["price"]:
                data["price"] = 0.0
            if "rooms" not in data:
                data["rooms"] = "brak informacji"
            if "heating" not in data:
                data["heating"] = "brak informacji"
            if "floor" not in data:
                data["floor"] = "brak informacji"
            if "rent" not in data:
                data["rent"] = 0.0
            if "state" not in data:
                data["state"] = "brak informacji"
            if "market" not in data:
                data["market"] = "brak informacji"
            if "ownership" not in data:
                data["ownership"] = "brak informacji"

            # Additional fields
            data["available"] = (
                "brak informacji"  # This field might not be available anymore
            )
            data["ad_type"] = ad_data.get("advertiserType", "brak informacji")

            # Additional features
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

            # Also check features without category
            features_without_category = ad_data.get("featuresWithoutCategory", [])
            features.extend(
                [
                    f.get("label", "")
                    for f in features_without_category
                    if isinstance(f, dict)
                ]
            )

            # Additional information
            additional_info = ad_data.get("additionalInformation", [])
            features.extend(
                [
                    info.get("value", "")
                    for info in additional_info
                    if isinstance(info, dict)
                ]
            )

            data["extra_info"] = ", ".join(filter(None, features)) or "brak informacji"

        return data

    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        import traceback

        print("Traceback:", traceback.format_exc())
        return {
            "slug": data["slug"],
            "url": url,
            "name": "brak informacji",
            "price": None,
            "area": None,
            "rooms": "brak informacji",
            "heating": "brak informacji",
            "floor": "brak informacji",
            "rent": None,
            "state": "brak informacji",
            "market": "brak informacji",
            "ownership": "brak informacji",
            "available": "brak informacji",
            "ad_type": "brak informacji",
            "extra_info": "brak informacji",
        }


def get_one_search_page(n: int) -> pd.DataFrame:
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
    df = pd.DataFrame()
    for i in range(offset, offset + n):
        print(f"\nProcessing page {i + 1} of {offset + n}")
        page_df = get_one_search_page(i)
        if not page_df.empty:
            df = pd.concat([df, page_df], ignore_index=False)
        else:
            print(f"No data found on page {i + 1}")
    return df


def main():
    parser = argparse.ArgumentParser(description="Scrape real estate data from OtoDom.")
    parser.add_argument(
        "--output",
        type=str,
        default="otodom.csv",
        help="output file name (default: otodom.csv)",
    )
    parser.add_argument(
        "--pages", type=int, default=1, help="number of pages to scrape (default: 1)"
    )
    parser.add_argument(
        "--offset", type=int, default=0, help="page number to start from (default: 0)"
    )

    args = parser.parse_args()

    print(f"Starting scraping {args.pages} page(s) from OtoDom...")
    print(f"Results will be saved to {args.output}")

    df = get_n_pages(args.pages, args.offset)

    if df.empty:
        print(
            "\nNo data was collected. Please check if the website structure has changed."
        )
        return

    df.to_csv(args.output)
    print(f"\nScraping completed. Found {len(df)} listings.")
    print(f"Data saved to {args.output}")


if __name__ == "__main__":
    main()
