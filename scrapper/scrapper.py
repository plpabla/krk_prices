import argparse
from scraping_utils import get_n_pages
import pandas as pd


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser for the scraper script."""
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
        "--offset", type=int, default=1, help="page number to start from (default: 1)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="enable debug mode (saves raw JSON data for each listing)",
    )
    return parser


def main():
    """Main entry point for the scraper CLI."""
    parser = create_parser()
    args = parser.parse_args()

    print(f"Starting scraping {args.pages} page(s) from OtoDom...")
    print(f"Results will be saved to {args.output}")
    if args.debug:
        print("Debug mode enabled - raw JSON data will be saved to logs/")

    df_prev = pd.DataFrame()
    try:
        df_prev = pd.read_csv(args.output)
        df_prev.set_index("slug", inplace=True)
    except:
        pass

    df = get_n_pages(args.pages, df_prev=df_prev, offset=args.offset, debug=args.debug)

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
