import pandas as pd
import xgboost as xgb
import pickle
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np
import sys


def run():
    # Wczytanie danych
    train_data = pd.read_csv("../data/otodom_district_train.csv")
    test_data = pd.read_csv("../data/otodom_district_test.csv")

    # Wybór cech i zmiennej docelowej
    X_train = train_data.drop(
        columns=["price", "price_m2"]
    )  # Załóżmy, że przewidujemy 'price'. Musimy też usunąć 'price_m2'
    y_train = train_data["price"]
    X_test = test_data.drop(columns=["price", "price_m2"])
    y_test = test_data["price"]

    # Inicjalizacja modelu
    model = xgb.XGBRegressor(
        objective="reg:squarederror",
        n_estimators=1_000,
        learning_rate=0.01,
        max_depth=8,
        random_state=42,
        n_jobs=-1,
    )

    # Trenowanie modelu
    model.fit(X_train, y_train)

    # Ocena modelu
    predictions = model.predict(X_test)

    # Obliczenie MSE, RMSE i R²
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f"  Mean Squared Error (MSE): {mse}")
    print(f"  Root Mean Squared Error (RMSE): {rmse}")
    print(f"  R-squared (R²): {r2}")

    # Zapisanie modelu do pliku
    with open("../out/xgboost_model.pkl", "wb") as file:
        pickle.dump(model, file)

    print("✅ Model XGBoost wytrenowany i zapisany!")


if __name__ == "__main__":
    run()
    # TODO: make it a parametrized script
    # if len(sys.argv) > 1:
    #     filename = sys.argv[1]
    #     create_train_test(filename)
    # else:
    #     print("Please provide a filename as argument")
    #     print("Usage: python create_train_test.py <filename>")
    #     sys.exit(1)
