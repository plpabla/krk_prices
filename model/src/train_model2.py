import sys
import pandas as pd
import xgboost as xgb
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import numpy as np
import optuna


def convert_str_to_category(
    train: pd.DataFrame, test: pd.DataFrame, city_name="otodom"
) -> tuple[pd.DataFrame, pd.DataFrame]:
    # Przekonwertuj kolumny kategoryczne na Categorical
    category_mappings = {}
    for col in train.select_dtypes(include=["object"]).columns:
        train[col] = train[col].astype("category")
        # Store the mapping for this column
        category_mappings[col] = dict(enumerate(train[col].cat.categories))

    # Zapisz mapowanie do pliku
    with open(f"../out/category_mappings_{city_name}.pkl", "wb") as file:
        pickle.dump(category_mappings, file)

    for col in test.select_dtypes(include=["object"]).columns:
        test[col] = test[col].astype("category")
    # Upewnij się, że kolumny kategoryczne mają te same kategorie w zbiorach treningowych i testowych
    for col in train.select_dtypes(include=["category"]).columns:
        test[col] = test[col].cat.set_categories(train[col].cat.categories)
    # Upewnij się, że kolumny kategoryczne mają te same kategorie w zbiorach treningowych i testowych
    for col in test.select_dtypes(include=["category"]).columns:
        train[col] = train[col].cat.set_categories(test[col].cat.categories)
    return train, test

def objective(trial):
    # Proponowanie hiperparametrów
    param = {
        "objective": "reg:squarederror",
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.5, 1.0),
        "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
        "n_estimators": 5000,
        "early_stopping_rounds": 50,
    }

    # Dzielimy dane na train i valid
    X_tr, X_val, y_tr, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

    model = xgb.XGBRegressor(**param)
    model.fit(
        X_tr, y_tr,
        eval_set=[(X_val, y_val)],
        verbose=False
    )

    preds = model.predict(X_val)
    rmse = mean_squared_error(y_val, preds, squared=False)
    return rmse


def run(filename: str = "otodom"):
    # Wczytanie danych
    train_data = pd.read_csv(f"../data/{filename}_district_train.csv")
    test_data = pd.read_csv(f"../data/{filename}_district_test.csv")

    # Wybór cech i zmiennej docelowej
    X_train = train_data.drop(columns=["price", "price_m2"])
    y_train = train_data["price"]
    X_test = test_data.drop(columns=["price", "price_m2"])
    y_test = test_data["price"]

    X_train, X_test = convert_str_to_category(X_train, X_test, city_name=filename)



    # Inicjalizacja modelu bazowego
    base_model = xgb.XGBRegressor(
        objective="reg:squarederror",
        random_state=42,
        enable_categorical=True,
    )

    model_grid = GridSearchCV(
        estimator=base_model,
        param_grid=params_grid,
        scoring="neg_root_mean_squared_error",
        cv=10,
        verbose=1,
        n_jobs=-1,
    )

    model_grid.fit(X_train, y_train)

    print("  ✅ Najlepsze parametry: ", model_grid.best_params_)
    print("  ✅ Najlepszy wynik (neg RMSE): ", model_grid.best_score_)


    # Zapisanie modelu do pliku
    with open(f"../out/{filename}_model.pkl", "wb") as file:
        pickle.dump(model_grid.best_estimator_, file)

    print("✅ Model XGBoost został wytrenowany i zapisany do pliku!")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        run(filename)
    else:
        run()
