import pickle
import xgboost as xgb
from schemas.estimate import EstimateInput


def import_model(filename: str):
    with open(filename, "rb") as file:
        model = pickle.load(file)
    return model
