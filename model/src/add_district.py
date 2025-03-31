import pandas as pd
import ast
import sys

from util import get_filename_and_extension


def add_district(source_filename: str) -> str:
    # Wczytaj dane z pliku CSV
    data = pd.read_csv(source_filename)

    # Dodaj kolumnę z dzielnicą; Format: ['Łobzów', 'Krowodrza', 'Kraków', 'małopolskie']
    data["location"] = data["location"].apply(ast.literal_eval)
    data["location_district"] = data["location"].apply(
        lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None
    )

    # Usuń wiersze, gdzie 'location_district' jest NaN
    data = data.dropna(subset=["location_district"])

    # Usuń dzielnice z pojedynczym wystąpieniem
    data = data[
        data.groupby("location_district")["location_district"].transform("count") > 1
    ]

    # Zapisz dane do pliku CSV
    base_name, extension = get_filename_and_extension(source_filename)
    output_filename = f"{base_name}_district{extension}"

    data.to_csv(output_filename, index=False)
    return output_filename


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        add_district(filename)
    else:
        print("Please provide a filename as argument")
        print("Usage: python add_district.py <filename>")
        sys.exit(1)
