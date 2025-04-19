import sys
import pandas as pd
import xgboost as xgb
import pickle
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV
import numpy as np


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

    params_grid = {
        "max_depth": [6],
        "learning_rate": [0.005],
        "n_estimators": [5000],
        "subsample": [0.3],
        "colsample_bytree": [0.8],
    }

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

    # Trenowanie GridSearch bez early stopping
    model_grid.fit(X_train, y_train)

    print("  ✅ Najlepsze parametry: ", model_grid.best_params_)
    print("  ✅ Najlepszy wynik (neg RMSE): ", model_grid.best_score_)

    # Pobranie najlepszego modelu i dalsze trenowanie z early stopping
    best_model = model_grid.best_estimator_
    best_model.fit(
        X_train,
        y_train,
        eval_set=[(X_test, y_test)],
        early_stopping_rounds=50,
        verbose=False
    )

    # Predykcja i ocena modelu
    predictions = best_model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f"  📊 Mean Squared Error (MSE): {mse:.2f}")
    print(f"  📊 Root Mean Squared Error (RMSE): {rmse:.2f}")
    print(f"  📊 R-squared (R²): {r2:.4f}")

    # Zapisanie modelu do pliku
    with open(f"../out/{filename}_model.pkl", "wb") as file:
        pickle.dump(best_model, file)

    print("✅ Model XGBoost został wytrenowany i zapisany do pliku!")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        filename = sys.argv[1]
        run(filename)
    else:
        run()
