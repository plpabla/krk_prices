import pickle
import xgboost as xgb
from xgboost import XGBRegressor
from schemas.estimate import EstimateInput


class Model:
    _instance = None
    _model: XGBRegressor | None = None

    def __new__(cls, model_path=None):
        if cls._instance is None:
            cls._instance = super(Model, cls).__new__(cls)
            if model_path:
                cls._model = Model._load_model(model_path)
        return cls._instance

    def __init__(self, model_path=None):
        # No initialization needed here since it's done in __new__
        pass

    def _load_model(model_path):
        """Load model from file."""
        with open(model_path, "rb") as file:
            # Load the model using pickle
            Model._model = pickle.load(file)

    def predict(self, data: EstimateInput):
        """Make prediction using the loaded model."""
        if not Model._model:
            raise ValueError("Model not loaded. Call load_model first.")

        # Preprocess data and make prediction
        # This depends on your specific model requirements
        return Model._model.predict([data.dict()])

    def get_districts(self) -> list[str]:
        features = Model._model.get_booster().feature_names
        return [
            feature.split("_")[-1]
            for feature in features
            if feature.startswith("location_district")
        ]
