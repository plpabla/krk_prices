import pandas as pd
import numpy as np
import re
import ast
import sys
from sklearn.preprocessing import MultiLabelBinarizer
import pickle
import warnings
from math import radians, cos, sin, asin, sqrt


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


def _calculate_iqr_price_m2(data):
    Q1 = data["price_m2"].quantile(0.25)
    Q3 = data["price_m2"].quantile(0.75)
    return (Q1, Q3)


def _drop_price_m2_outlier_rows(data, Q1_Q3: tuple[float, float]):
    Q1, Q3 = Q1_Q3
    IQR = Q3 - Q1

    return _drop_row_if_condition(
        data,
        lambda row: (row["price_m2"] < (Q1 - 1.5 * IQR))
        or (row["price_m2"] > (Q3 + 1.5 * IQR)),
    )

from math import radians, cos, sin, asin, sqrt


def _haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees).
    Returns distance in kilometers.
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r


def _add_distance_from_center(data):
    center_lat = 50.0619474
    center_lon = 19.9368564
    data["distance_from_center"] = data.apply(
        lambda row: _haversine(row["location_lat"], row["location_lon"], center_lat, center_lon),
        axis=1
    )
    return data



def _clear_wrong_build_year(data):
    data = _drop_row_if_na(data, "build_year")
    return _drop_row_if_condition(
        data,
        lambda row: (row["build_year"] < 1000) or (row["build_year"] > 2030),
    )


def _process_floor(value, default_floor=0):
    if pd.isna(value) or value.strip() == "":
        return default_floor
    if value == "cellar":
        return -1
    if value == "ground_floor":
        return 0
    match = re.search(r"\d+", value)
    return int(match.group()) if match else default_floor


def _get_building_floors_per_district(data):
    # Get the median number of floors for each district
    building_floors_district_median = (
        data.groupby("location_district")["building_floors"]
        .median()
        .fillna(-1)  # Fill NaN values temporarily
        .astype(int)
        .reset_index()
    )
    # Replace -1 back with None
    building_floors_district_median.loc[
        building_floors_district_median["building_floors"] == -1,
        "building_floors",
    ] = None
    # Rename the columns for clarity
    building_floors_district_median.columns = [
        "location_district",
        "building_floors_median",
    ]
    return building_floors_district_median


def _fill_building_floors_with_common_in_given_district(data, district_median):
    # fill NaN values in 'building_floors' with the median building floors for the district
    data = data.merge(
        district_median,
        on="location_district",
        how="left",
    )
    data.loc[:, "building_floors"] = data.apply(
        lambda row: (
            row["building_floors_median"]
            if pd.isna(row["building_floors"])
            else row["building_floors"]
        ),
        axis=1,
    )
    data.drop(
        columns=[c for c in district_median.columns if c != "location_district"],
        inplace=True,
    )

    data = _drop_row_if_na(data, "building_floors")
    # Convert 'building_floors' to integer
    data.loc[:, "building_floors"] = data["building_floors"].astype(int)
    # Check if the building_floors is greater than or equal to the floor
    data = _drop_row_if_condition(
        data,
        lambda row: (
            row["building_floors"] < row["floor"] if pd.notna(row["floor"]) else False
        ),
    )
    return data


def _safe_convert_to_int(value):
    return int(value) if str(value).isdigit() else np.nan


def _calculate_rooms_per_area(data):
    # FIXME: it doesn't work
    area_bins = pd.cut(data["area"], bins=10)
    rooms_per_area_bin = data.groupby(area_bins, observed=True)["rooms"].median()
    # This creates a mapping we can use to fill missing values based on property area
    area_to_rooms_map = {
        bin_name: rooms for bin_name, rooms in rooms_per_area_bin.items()
    }
    # Expected return: array with (max_area, rooms) tuples
    for bin_name, rooms in area_to_rooms_map.items():
        area_to_rooms_map[bin_name] = _safe_convert_to_int(rooms)
    # Convert the area_bins to a list of tuples
    area_bins = [
        (bin.left, bin.right) for bin in area_bins.categories
    ]  # Convert to list of tuples


def _fill_empty_rooms(data, area_bins, area_to_rooms_map):
    # FIXME: it doesn't work
    # Fill missing values in 'rooms' based on the mapping
    data.loc[:, "rooms"] = data.apply(
        lambda row: (
            area_to_rooms_map.get(area_bins[row.name], data["rooms"].median())
            if pd.isna(row["rooms"])
            else row["rooms"]
        ),
        axis=1,
    )

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
    data.drop(
        columns=[c for c in district_median.columns if c != "location_district"],
        inplace=True,
    )
    data = _drop_row_if_na(data, "build_year")
    # Convert 'build_year' to integer
    data.loc[:, "build_year"] = data["build_year"].astype(int)

    return data


def _calculate_median_values(data):
    # Get the median build year for each district
    build_year_district_median = _get_build_year_district_median(data)
    # Get the median number of floors for each district
    building_floors_district_median = _get_building_floors_per_district(data)

    # Merge the two DataFrames on 'location_district'
    district_median = pd.merge(
        build_year_district_median,
        building_floors_district_median,
        on="location_district",
        how="outer",
    )

    return district_median


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


def preprocess_data(
    data: pd.DataFrame, is_train: bool, config_filename: str
) -> pd.DataFrame:
    if is_train:
        config = {}
    else:
        with open(config_filename, "rb") as f:
            config = pickle.load(f)

    data = _drop_row_if_na(data, "price")
    data = _drop_row_if_condition(
        data,
        lambda row: "tbs" in row["name"].lower(),
    )
    data = _add_price_m2_column(data)
    data = _add_distance_from_center(data)

    if is_train:
        config["q1_q3"] = _calculate_iqr(data)
        config["q1_q3_m2"] = _calculate_iqr_price_m2(data)
        config["district_median"] = _calculate_median_values(data)
        # Doesn't work
        # config["area_to_rooms_map"], config["area_bins"] = _calculate_rooms_per_area(
        #     data
        # )
        with open(config_filename, "wb") as f:
            pickle.dump(config, f)

    data = _drop_price_outlier_rows(data, config["q1_q3"])
    data = _drop_price_m2_outlier_rows(data, config["q1_q3_m2"])
    data = _fill_build_year_with_district_median(data, config["district_median"])
    data = _clear_wrong_build_year(data)

    data["floor"] = data["floor"].apply(_process_floor)
    data = _fill_building_floors_with_common_in_given_district(
        data, config["district_median"]
    )

    # Przetwarzanie liczby pokoi - nie dziala
    # data = _fill_empty_rooms(data, config["area_bins"], config["area_to_rooms_map"])
    data["rooms"] = data["rooms"].apply(_safe_convert_to_int)
    data = _drop_row_if_na(data, "rooms")

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
