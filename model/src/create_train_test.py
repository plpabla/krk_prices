import sys
import pandas as pd
from sklearn.model_selection import train_test_split

from util import get_filename_and_extension


def create_train_test(source_filename: str, test_size: float = 0.2) -> tuple[str, str]:
    # Wczytaj dane z pliku CSV
    data = pd.read_csv(source_filename)

    train, test = train_test_split(
        data, test_size=test_size, random_state=42, stratify=data["location_district"]
    )

    base_name, extension = get_filename_and_extension(source_filename)
    train_filename = f"{base_name}_train{extension}"
    test_filename = f"{base_name}_test{extension}"

    # Zapisz
    train.to_csv(train_filename, index=False)
    test.to_csv(test_filename, index=False)

    return train_filename, test_filename


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        create_train_test(filename)
    else:
        print("Please provide a filename as argument")
        print("Usage: python create_train_test.py <filename>")
        sys.exit(1)
