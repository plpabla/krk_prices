import argparse
from scrapper.scraping_utils import get_n_pages


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
        "--offset", type=int, default=0, help="page number to start from (default: 0)"
    )
    return parser


def main():
    """Main entry point for the scraper CLI."""
    parser = create_parser()
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
