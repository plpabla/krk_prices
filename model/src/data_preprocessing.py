import pandas as pd
import numpy as np
import re
import ast
import sys
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import date, timedelta
import warnings


def _drop_row_if_na(data, col_name):
    data = data.dropna(subset=[col_name])
    data.reset_index(drop=True, inplace=True)
    return data


def _drop_row_if_condition(data, condition):
    data = data[~data.apply(condition, axis=1)]
    data.reset_index(drop=True, inplace=True)
    return data


def _calculate_iqr(data):
    Q1 = data["price"].quantile(0.25)
    Q3 = data["price"].quantile(0.75)
    return (Q1, Q3)


def _drop_price_outlier_rows(data, Q1_Q3: tuple[float, float]):
    Q1, Q3 = Q1_Q3
    IQR = Q3 - Q1

    return _drop_row_if_condition(
        data,
        lambda row: (row["price"] < (Q1 - 1.5 * IQR))
        or (row["price"] > (Q3 + 1.5 * IQR)),
    )


def _clear_wrong_build_year(data):
    data = _drop_row_if_na(data, "build_year")
    return _drop_row_if_condition(
        data,
        lambda row: (row["build_year"] < 1000) or (row["build_year"] > 2030),
    )


def _process_floor(value, default_floor=0):
    if pd.isna(value) or value.strip() == "":
        return np.nan
    if value == "cellar":
        return -1
    if value == "ground_floor":
        return 0
    match = re.search(r"\d+", value)
    return int(match.group()) if match else default_floor


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


def _get_build_year_district_median(data):
    # Get the median build year for each district
    build_year_district_median = (
        data.groupby("location_district")["build_year"]
        .median()
        .fillna(-1)  # Fill NaN values temporarily
        .astype(int)
        .reset_index()
    )
    # Replace -1 back with None
    build_year_district_median.loc[
        build_year_district_median["build_year"] == -1, "build_year"
    ] = None
    # Rename the columns for clarity
    build_year_district_median.columns = ["location_district", "build_year_median"]
    return build_year_district_median


def _fill_build_year_with_district_median(data, district_median):
    # fill NaN values in 'build_year' with the median build year for the district
    data = data.merge(
        district_median,
        on="location_district",
        how="left",
    )
    data.loc[:, "build_year"] = data.apply(
        lambda row: (
            row["build_year_median"]
            if pd.isna(row["build_year"])
            else row["build_year"]
        ),
        axis=1,
    )
    data.drop(columns=["build_year_median"], inplace=True)
    data = _drop_row_if_na(data, "build_year")
    # Convert 'build_year' to integer
    data.loc[:, "build_year"] = data["build_year"].astype(int)

    return data


def _add_price_m2_column(data):
    data["price_m2"] = data["price"] / data["area"]

    # TODO: Maybe we should use median from district?
    avg_price_m2 = data["price_m2"].mean()
    data["price_m2"] = data["price_m2"].fillna(avg_price_m2)
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
    if is_train:
        config = {}
    else:
        # TODO: load config from file
        config = {
            "q1_q3": (0, 1000000),
            "district_median": pd.DataFrame(
                columns=["location_district", "build_year_median"],
                data={
                    "Bieżanów-Prokocim": 2023,
                    "Bronowice": None,
                    "Dębniki": 2024,
                    "Grzegórzki": 2025,
                    "Krowodrza": 2018,
                    "Podgórze": 2024,
                    "Prądnik Biały": 2026,
                    "Prądnik Czerwony": 1970,
                    "Stare Miasto": None,
                    "Zwierzyniec": 2025,
                },
            ),
        }

    data = _drop_row_if_na(data, "price")
    data = _drop_row_if_condition(
        data,
        lambda row: "tbs" in row["name"].lower(),
    )
    # TODO: Check what if we remove all offers > 2M

    if is_train:
        config["q1_q3"] = _calculate_iqr(data)
        config["district_median"] = _get_build_year_district_median(data)

    data = _drop_price_outlier_rows(data, config["q1_q3"])

    data = _fill_build_year_with_district_median(data, config["district_median"])
    data = _clear_wrong_build_year(data)

    data["floor"] = data["floor"].apply(_process_floor)
    # data = _fill_empty_floor(data)
    if is_train:
        data = _fill_building_floors_with_common_in_given_district(data)
    else:
        # TODO: or utilize data from train set instead of dropping
        data = _drop_row_if_na(data, "building_floors")
        data.loc[:, "building_floors"] = data["building_floors"].astype(int)

    # Przetwarzanie liczby pokoi
    if is_train:
        data = _fill_empty_rooms(data)
    else:
        # TODO: utilize data from training set to fill up instead of dropping
        data = _drop_row_if_na(data, "rooms")
        data.loc[:, "rooms"] = data["rooms"].apply(_safe_convert_to_int)

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
