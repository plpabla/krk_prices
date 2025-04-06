import sys
import pandas as pd

from add_district import add_district
from create_train_test import create_train_test
from data_preprocessing import preprocess_data
from util import get_filename_and_extension


if __name__ == "__main__":
    if len(sys.argv) > 1:
        source_filename = sys.argv[1]
    else:
        print("Please provide a filename as argument")
        print("Usage: python create_train_test.py <filename>")
        # sys.exit(1)
        source_filename = "model/data/testowy.csv"

    filename = add_district(source_filename)
    print("✅ Plik z dzielnicami utworzony")

    train_filename, test_filename = create_train_test(filename)
    print("✅ Pliki train/test utworzone")

    train = pd.read_csv(train_filename)
    test = pd.read_csv(test_filename)

    # Przetworzenie i zapis zestawów train/test
    name, _ = get_filename_and_extension(source_filename)
    config_filename = f"{name}.pkl"
    train = preprocess_data(train, is_train=True, config_filename=config_filename)
    test = preprocess_data(test, is_train=False, config_filename=config_filename)

    # Porównanie kolumn i dodanie brakujących kolumn z zerami
    for col in train.columns:
        if col not in test.columns:
            test[col] = 0

    for col in test.columns:
        if col not in train.columns:
            train[col] = 0

    # Zapewnienie, że kolumny w train i test są w tej samej kolejności
    train = train[sorted(train.columns)]
    test = test[sorted(test.columns)]

    train.to_csv(train_filename, index=False)
    test.to_csv(test_filename, index=False)

    print(f"✅ Dane przetworzone i zapisane jako {train_filename} oraz {test_filename}")
