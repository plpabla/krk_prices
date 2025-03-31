import pandas as pd
import numpy as np
import re
import ast
import sys
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import date, timedelta
import warnings

# TODO: for test set we cannot make the same preprocessing steps as for train set


def _drop_offers_without_price(data):
    return data.dropna(subset=["price"])


def _drop_tbs(data):
    return data[~data["name"].str.contains("tbs", case=False, na=False)]


def _calculate_iqr(data):
    Q1 = data["price"].quantile(0.25)
    Q3 = data["price"].quantile(0.75)
    return (Q1, Q3)


def _drop_price_outlier_rows(data, Q1_Q3: tuple[float, float]):
    Q1, Q3 = Q1_Q3
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


# TODO: Refactor this to have a function for dropping given column
def _drop_offers_without_building_floors(data):
    data = data.dropna(subset=["building_floors"])
    data.loc[:, "building_floors"] = data["building_floors"].astype(int)
    data.reset_index(drop=True, inplace=True)
    return data


def _drop_offers_without_build_year(data):
    data = data.dropna(subset=["build_year"])
    data.loc[:, "build_year"] = data["build_year"].apply(_safe_convert_to_int)
    return data


def _safe_convert_to_int(value):
    return int(value) if str(value).isdigit() else np.nan


def _fill_empty_rooms(data):
    # convert to int
    data.loc[:, "rooms"] = data["rooms"].apply(_safe_convert_to_int)

    # Create a map of median number of rooms per given area, using 10 bins
    area_bins = pd.cut(data["area"], bins=10)
    rooms_per_area_bin = data.groupby(area_bins, observed=True)["rooms"].median()
    # This creates a mapping we can use to fill missing values based on property area
    area_to_rooms_map = {
        bin_name: rooms for bin_name, rooms in rooms_per_area_bin.items()
    }

    # Fill missing values in 'rooms' based on the mapping
    data.loc[:, "rooms"] = data.apply(
        lambda row: (
            area_to_rooms_map[area_bins[row.name]]
            if pd.isna(row["rooms"])
            else row["rooms"]
        ),
        axis=1,
    )

    data.loc[:, "rooms"] = data["rooms"].apply(_safe_convert_to_int)
    return data


def _drop_empty_rooms(data):
    # Drop rows with empty rooms
    data = data.dropna(subset=["rooms"])
    # Convert rooms to int
    data.loc[:, "rooms"] = data["rooms"].apply(_safe_convert_to_int)
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


def _utilities_one_hot_encoding(data, items):
    data["utilities"] = data["utilities"].apply(ast.literal_eval)
    mlb = MultiLabelBinarizer(classes=items)

    # We are fully aware that we are skipping some classes
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", message="unknown class")
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


def preprocess_data(data: pd.DataFrame, is_train=True):
    data = _drop_offers_without_price(data)
    data = _drop_tbs(data)

    # TODO: move is_train logic into one place
    # TODO: for train set, store IQR, for test set use it
    if is_train:
        q1_q3 = _calculate_iqr(data)
        data = _drop_price_outlier_rows(data, q1_q3)
    else:
        data = _drop_price_outlier_rows(data, (0, 1000000))

    # Update index after cleanup
    data.reset_index(drop=True, inplace=True)

    data = _clear_wrong_build_year(data)
    data["floor"] = data["floor"].apply(_process_floor)
    # data = _fill_empty_floor(data)
    if is_train:
        data = _fill_building_floors_with_common_in_given_district(data)
    else:
        # TODO: or utilize data from train set
        data = _drop_offers_without_building_floors(data)

    # Przetwarzanie liczby pokoi
    # FIXME: now I'm getting only empty values here... (so I overwrite them with 99999)
    if is_train:
        data = _fill_empty_rooms(data)
    else:
        data = _drop_empty_rooms(data)
    # data.loc[:, "rooms"] = 99999

    # TODO: or utilize data from train set
    # FIXME: not filled in
    if is_train:
        data = _fill_build_year_with_district_median(data)
    else:
        data = _drop_offers_without_build_year(data)
    # data.loc[:, "build_year"] = 99999

    # TODO: is it used anywhere?
    data = _add_price_m2_column(data)

    # One-Hot Encoding
    utilities = [
        "balkon",
        "taras",
        "oddzielna kuchnia",
        "piwnica",
        "pom. użytkowe",
        "winda",
    ]
    utilities_outside_the_form = [
        "dwupoziomowe",
        "garaż/miejsce parkingowe",
        "klimatyzacja",
        "meble",
        "ogródek",
    ]
    data.reset_index(drop=True, inplace=True)
    data = _utilities_one_hot_encoding(data, utilities)

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

    extra_columns_to_drop = [
        "available",
        "heating_boiler_room",
        "heating_electrical",
        "heating_gas",
        "heating_other",
        "heating_tiled_stove",
        "heating_urban",
        "market_primary",
        "market_secondary",
        "ownership_full_ownership",
        "ownership_limited_ownership",
        "ownership_share",
        "ownership_usufruct",
        "rent",
        "state_ready_to_use",
        "state_to_completion",
        "state_to_renovation",
    ]

    # Only drop columns that exist in the DataFrame
    extra_columns_to_drop = [
        col for col in extra_columns_to_drop if col in data.columns
    ]
    data.drop(columns=extra_columns_to_drop, inplace=True)

    return data


if __name__ == "__main__":
    # data = pd.read_csv("model/data/krakow_district_train.csv")
    # preprocess_data(data, is_train=True)

    print("This script is not intended to be run directly, run pipeline script instead")
    sys.exit(1)
