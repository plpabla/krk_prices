import pickle
import numpy as np
from xgboost import XGBRegressor

from schemas.estimate import EstimateInput
from model.util import (
    calculate_lat_lon,
    calc_distance_from_center,
    calc_distance_from_other_expensive,
)

__all__ = ["model"]


class Model:
    _model: XGBRegressor | None = None
    _cat_features_mapping: dict[str, dict[int, str]] = {}

    def __init__(self, model_path=None, cat_file_path=None):
        self._load_model(model_path, cat_file_path)

    def _load_model(self, model_path, cat_file_path):
        """Load model from file."""
        with open(model_path, "rb") as file:
            # Load the model using pickle
            self._model = pickle.load(file)
        with open(cat_file_path, "rb") as file:
            self._cat_features_mapping = pickle.load(file)
        print(">>> Model loaded successfully.")

    def predict(self, data: EstimateInput):
        """Make prediction using the loaded model."""
        data = self.convert_to_xgboost_input(data)
        print(">>> Raw data for prediction:", data)
        return self._model.predict(data)

    def predict_raw(self, data: np.array):
        """Make prediction using the loaded model with raw data."""
        if self._model is None:
            raise ValueError("Model is not loaded.")
        return self._model.predict(data)

    def get_districts(self) -> list[str]:
        return [v for v in self._cat_features_mapping["location_district"].values()]

    def convert_to_xgboost_input(self, data: EstimateInput) -> np.array:
        features = validate_schema(self._model)
        n_features = len(features)
        data_array = np.zeros([n_features])

        form_data = {}
        # Categorical features
        form_data["ad_type"] = self._map("ad_type", data.ad_type)
        form_data["heating"] = self._map("heating", data.heating)
        form_data["location_district"] = self._map("location_district", data.district)
        form_data["market"] = self._map("market", data.market)
        form_data["ownership"] = self._map("ownership", data.ownership)
        form_data["state"] = self._map("state", data.state)

        form_data["area"] = data.area
        form_data["build_year"] = 2000  # TODO: missing in backend
        form_data["building_floors"] = data.floorsInBuilding
        form_data["floor"] = data.floor

        lat, lon = calculate_lat_lon(data.location)
        form_data["location_lat"] = lat
        form_data["location_lon"] = lon
        form_data["rooms"] = data.rooms
        form_data["utilities_balkon"] = int(data.balcony)
        form_data["utilities_oddzielna kuchnia"] = int(data.separate_kitchen)
        form_data["utilities_piwnica"] = int(data.basement)
        form_data["utilities_pom. użytkowe"] = int(data.basement)
        form_data["utilities_taras"] = int(data.balcony)
        form_data["utilities_winda"] = int(data.elevator)
        # form_data["utilities_garage"] = int(data.garage) # TODO: add in model or remove from frontend
        # TODO: available in frontend but not used: available from
        form_data["distance_from_center"] = calc_distance_from_center(lat, lon)
        form_data["distance_from_other_expensive"] = calc_distance_from_other_expensive(
            lat, lon
        )

        print(">>> Form data for prediction:", form_data)

        # Fill data_array with values from form_data using fetures array
        for i, feature in enumerate(features):
            if feature in form_data:
                data_array[i] = form_data[feature]
            else:
                raise ValueError(f"Feature '{feature}' not found in form_data")

        # Reshape the 1D array to a 2D array (1 x 38) as required by XGBoost
        data_array = np.reshape(data_array, (1, -1))
        return data_array

    def _map(self, feature: str, value: str) -> int:
        translated_value = translate(feature, value)
        if feature in self._cat_features_mapping:
            mapping = self._cat_features_mapping[feature]
            for key, val in mapping.items():
                if val == translated_value:
                    return key
        raise ValueError(
            f"Value '{value}' not found in mapping for feature '{feature}'"
        )


model = Model(
    "../model/out/krakow_model.pkl", "../model/out/category_mappings_krakow.pkl"
)


def validate_schema(model: XGBRegressor) -> int:
    """ " Validate schema of the model. Version 2.1.1"""
    features = model.get_booster().feature_names
    expected_feature_names = [
        "ad_type",
        "area",
        "build_year",
        "building_floors",
        "floor",
        "heating",
        "location_district",
        "location_lat",
        "location_lon",
        "market",
        "ownership",
        "rooms",
        "state",
        "utilities_balkon",
        "utilities_oddzielna kuchnia",
        "utilities_piwnica",
        "utilities_pom. użytkowe",
        "utilities_taras",
        "utilities_winda",
        "distance_from_center",
        "distance_from_other_expensive",
    ]

    # Check if all expected features are present regardless of order
    for feature in expected_feature_names:
        assert feature in features, f"Expected feature '{feature}' is missing"

    assert len(features) == len(
        expected_feature_names
    ), f"Expected {len(expected_feature_names)} features, got {len(features)}"

    return features


def translate(feature: str, value: str) -> str:
    """Translate feature value to its original value."""
    if feature == "location_district":
        return value

    dictionary = {
        "ad_type": {"prywatny": "private", "biuro": "business"},
        "heating": {
            "miejskie": "boiler_room",
            "gazowe": "gas",
            "elektryczne": "electric",
            "inne": "other",
        },  # TODO: inne są w modelu
        "market": {"Pierwotny": "primary", "Wtórny": "secondary"},
        "ownership": {
            "Własnościowe": "full_ownership",
            "Spoldzielcze": "usufruct",
            "Inne": "share",
        },  # TODO: inne są w modelu
        "state": {
            "Do zamieszkania": "ready_to_use",
            "Do remontu": "to_renovation",
            "Do wykończenia": "to_completion",
        },
    }
    res: str | None = dictionary.get(feature, {}).get(value, value)
    if res is None:
        raise ValueError(
            f"Value '{value}' not found in dictionary for feature '{feature}'"
        )
    return res
