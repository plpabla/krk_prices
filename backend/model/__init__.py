import pickle
import numpy as np
from xgboost import XGBRegressor

from schemas.estimate import EstimateInput, MarketType, OwnershipType, AdType

__all__ = ["model"]


class Model:
    _model: XGBRegressor | None = None

    def __init__(self, model_path=None):
        self._load_model(model_path)

    def _load_model(self, model_path):
        """Load model from file."""
        with open(model_path, "rb") as file:
            # Load the model using pickle
            self._model = pickle.load(file)
        print(">>> Model loaded successfully.")

    def predict(self, data: EstimateInput):
        """Make prediction using the loaded model."""
        data = self.convert_to_xgboost_input(data)
        print(">>> Raw data for prediction:", data)
        return self._model.predict(data)

    def get_districts(self) -> list[str]:
        features = self._model.get_booster().feature_names
        return [
            feature.split("_")[-1]
            for feature in features
            if feature.startswith("location_district")
        ]

    def convert_to_xgboost_input(self, data: EstimateInput) -> np.array:
        validate_schema(self._model)
        data_array = np.zeros([38])
        data_array[0] = int(data.ad_type == AdType.AGENCY)
        data_array[1] = int(data.ad_type == AdType.PRIVATE)
        data_array[2] = data.area
        data_array[3] = 2000  # TODO: missing in frontend
        data_array[4] = data.floorsInBuilding
        data_array[5] = data.floor
        data_array[6] = int(data.district == "Bieńczyce")
        data_array[7] = int(data.district == "Bieżanów-Prokocim")
        data_array[8] = int(data.district == "Bronowice")
        data_array[9] = int(data.district == "Czyżyny")
        data_array[10] = int(data.district == "Dębniki")
        data_array[11] = int(data.district == "Grzegórzki")
        data_array[12] = int(data.district == "Krowodrza")
        data_array[13] = int(data.district == "Mistrzejowice")
        data_array[14] = int(data.district == "Mogilany")
        data_array[15] = int(data.district == "Nowa Huta")
        data_array[16] = int(data.district == "Podgórze")
        data_array[17] = int(data.district == "Podgórze Duchackie")
        data_array[18] = int(data.district == "Prądnik Biały")
        data_array[19] = int(data.district == "Prądnik Czerwony")
        data_array[20] = int(data.district == "Skawina")
        data_array[21] = int(data.district == "Stare Miasto")
        data_array[22] = int(data.district == "Swoszowice")
        data_array[23] = int(data.district == "Wieliczka")
        data_array[24] = int(data.district == "Wielka Wieś")
        data_array[25] = int(data.district == "Wzgórza Krzesławickie")
        data_array[26] = int(data.district == "Zielonki")
        data_array[27] = int(data.district == "Zwierzyniec")
        data_array[28] = int(data.district == "Łagiewniki-Borek Fałęcki")
        data_array[29] = 50.0647  # TODO: missing calculation from address
        data_array[30] = 19.9450  # TODO: missing calculation from address
        data_array[31] = data.rooms
        data_array[32] = int(data.balcony)
        data_array[33] = int(data.separate_kitchen)
        data_array[34] = int(data.basement)
        data_array[35] = int(data.basement)
        data_array[36] = int(data.balcony)
        data_array[37] = int(data.elevator)

        # Reshape the 1D array to a 2D array (1 x 38) as required by XGBoost
        data_array = np.reshape(data_array, (1, -1))
        return data_array


model = Model("../model/out/xgboost_model.pkl")


def validate_schema(model: XGBRegressor):
    """ " Validate schema of the model. Version 1.0.0"""
    features = model.get_booster().feature_names
    assert len(features) == 38, f"Expected 38 features, got {len(features)}"
    expected_feature_names = [
        "ad_type_business",
        "ad_type_private",
        "area",
        "build_year",
        "building_floors",
        "floor",
        "location_district_Bieńczyce",
        "location_district_Bieżanów-Prokocim",
        "location_district_Bronowice",
        "location_district_Czyżyny",
        "location_district_Dębniki",
        "location_district_Grzegórzki",
        "location_district_Krowodrza",
        "location_district_Mistrzejowice",
        "location_district_Mogilany",
        "location_district_Nowa Huta",
        "location_district_Podgórze",
        "location_district_Podgórze Duchackie",
        "location_district_Prądnik Biały",
        "location_district_Prądnik Czerwony",
        "location_district_Skawina",
        "location_district_Stare Miasto",
        "location_district_Swoszowice",
        "location_district_Wieliczka",
        "location_district_Wielka Wieś",
        "location_district_Wzgórza Krzesławickie",
        "location_district_Zielonki",
        "location_district_Zwierzyniec",
        "location_district_Łagiewniki-Borek Fałęcki",
        "location_lat",
        "location_lon",
        "rooms",
        "utilities_balkon",
        "utilities_oddzielna kuchnia",
        "utilities_piwnica",
        "utilities_pom. użytkowe",
        "utilities_taras",
        "utilities_winda",
    ]

    assert (
        features == expected_feature_names
    ), "Feature names don't match or are in wrong order"
