import pandas as pd
import numpy as np
import re
import ast
import os
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import date, timedelta

from add_district import add_district
from create_train_test import create_train_test

# TODO: move to the bottom whre if __name__ == "__main__" is
filename = os.path.join("..", "data", "krakow.csv")
filename = add_district(filename)
train_filename, test_filename = create_train_test(filename)

train = pd.read_csv(train_filename)
test = pd.read_csv(test_filename)


def _drop_offers_without_price(data):
    return data.dropna(subset=["price"])


def _drop_tbs(data):
    return data[~data["name"].str.contains("tbs", case=False, na=False)]


def _drop_price_outlier_rows(data):
    Q1 = data["price"].quantile(0.25)
    Q3 = data["price"].quantile(0.75)
    IQR = Q3 - Q1

    # Odrzucenie wartości poza zakresem IQR
    data = data[(data["price"] >= Q1 - 1.5 * IQR) & (data["price"] <= Q3 + 1.5 * IQR)]
    return data


def _clear_wrong_build_year(data):
    return data.loc[(data["build_year"] >= 1000) & (data["build_year"] <= 2030)]


def _process_floor(value):
    if pd.isna(value) or value.strip() == "":
        return np.nan
    if value == "cellar":
        return -1
    if value == "ground_floor":
        return 0
    match = re.search(r"\d+", value)
    return int(match.group()) if match else np.nan


def _fill_empty_floor(data):
    data.loc[:, "floor"] = data["floor"].fillna(data["floor"].mode()[0])


def _fill_building_floors_with_common_in_given_district(data):
    data.loc[:, "building_floors"] = data.groupby("location_district")[
        "building_floors"
    ].transform(
        lambda x: x.fillna(
            x.mode()[0] if not x.mode().empty else data["building_floors"].mode()[0]
        )
    )
    # data.loc[:, "building_floors"] = data["building_floors"].astype(int)
    return data


def _convert_to_int(value):
    return int(value) if str(value).isdigit() else None


def _fill_empty_rooms(data):
    data.loc[:, "rooms"] = data.groupby(pd.cut(data["area"], bins=10), observed=True)[
        "rooms"
    ].transform("median")

    if data["rooms"].isna().sum() > 0:
        # Obliczamy średnią powierzchnię pokoju
        avg_room_size = data["area"].sum() / data["rooms"].sum()

        # Zastępujemy brakujące wartości na podstawie średniej powierzchni pokoju
        data.loc[:, "rooms"] = data["rooms"].fillna(
            (data["area"] / avg_room_size).round()
        )
    return data


def _fill_rent(data):
    # Podstawowe dane dla Krakowa
    min_rent_per_m2 = 6.64
    max_rent_per_m2 = 16.96

    # Krok 1: Sprawdzanie, czy rent mieści się w przedziale 6,64 * area < rent < 16,96 * area
    data["rent"] = data.apply(
        lambda row: (
            row["rent"]
            if (
                min_rent_per_m2 * row["area"]
                < row["rent"]
                < max_rent_per_m2 * row["area"]
            )
            else 10 * row["area"]
        ),
        axis=1,
    )

    return data


def _fill_build_year_with_district_median(data):
    data.loc[:, "build_year"] = data["build_year"].fillna(
        data.groupby("location_district")["build_year"].transform("median")
    )
    data.loc[:, "build_year"] = data[
        "build_year"
    ].round()  # Zaokrąglanie do pełnej liczby
    return data


def _add_price_m2_column(data):
    data["price_m2"] = data["price"] / data["area"]

    # TODO: Maybe we should use median from district?
    avg_price_m2 = data["price_m2"].mean()
    data["price_m2"] = data["price_m2"].fillna(avg_price_m2)
    return data


def _transform_available_date(data):
    # Upewnij się, że kolumna 'available' jest w formacie datetime.date
    data["available"] = pd.to_datetime(data["available"], errors="coerce").dt.date

    # Uzupełnienie brakujących wartości w 'available' pierwszym dniem bieżącego roku
    data.loc[:, "available"] = data["available"].fillna(date(date.today().year, 1, 1))

    # Zamiana dat wcześniejszych niż dzisiejszy dzień na dzisiejszą datę
    # oraz dat późniejszych niż 2 lata od dzisiaj na dzisiejszą datę
    data["available"] = data["available"].apply(
        lambda x: min(max(x, date.today()), date.today() + timedelta(days=730))
    )

    # Konwersja 'available' na liczbę dni od 1 stycznia bieżącego roku
    data["available"] = (
        pd.to_datetime(data["available"], errors="coerce")
        - pd.to_datetime(date(date.today().year, 1, 1))
    ).dt.days
    return data


def _utilities_one_hot_encoding(data):
    # TODO: create a list of utilities I'd like to encode
    data["utilities"] = data["utilities"].apply(ast.literal_eval)
    mlb = MultiLabelBinarizer()
    utilities_encoded = mlb.fit_transform(data["utilities"])
    utilities_df = pd.DataFrame(
        utilities_encoded, columns=["utilities_" + col for col in mlb.classes_]
    )
    data = data.join(utilities_df)
    return data


def _columns_one_hot_encoding(data, columns):
    for feature in columns:
        encoded = pd.get_dummies(data[feature], prefix=feature)
        data = data.join(encoded)
        data[encoded.columns] = data[encoded.columns].astype(int)
    return data


def preprocess_data(data):
    # TODO: Check - do I really need to assing data here? this function should work on a data directly
    data = _drop_offers_without_price(data)
    data = _drop_tbs(data)
    data = _drop_price_outlier_rows(data)

    data = _clear_wrong_build_year(data)
    data["floor"] = data["floor"].apply(_process_floor)
    # data = _fill_empty_floor(data)
    data = _fill_building_floors_with_common_in_given_district(data)

    # Przetwarzanie liczby pokoi
    data.loc[:, "rooms"] = data["rooms"].apply(_convert_to_int)
    data = _fill_empty_rooms(data)

    data = _fill_rent(data)
    data = _fill_build_year_with_district_median(data)

    data = _add_price_m2_column(data)

    data = _transform_available_date(data)

    # One-Hot Encoding
    data = _utilities_one_hot_encoding(data)

    categorical_features = [
        "heating",
        "state",
        "market",
        "ownership",
        "ad_type",
        "location_district",
    ]
    data = _columns_one_hot_encoding(data, categorical_features)

    # Usunięcie zbędnych kolumn
    data.drop(
        columns=[
            "utilities",
            "heating",
            "state",
            "market",
            "ownership",
            "location",
            "ad_type",
            "scrapped_date",
            "slug",
            "url",
            "name",
            "location_district",
        ],
        inplace=True,
    )

    return data


# Przetworzenie i zapis zestawów train/test
train = preprocess_data(train)
test = preprocess_data(test)

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

##todo make path operating system independent with os.path.join
train.to_csv("../data/otodom_train.csv", index=False)
test.to_csv("../data/otodom_test.csv", index=False)

print("✅ Dane przetworzone i zapisane jako train.csv oraz test.csv")
