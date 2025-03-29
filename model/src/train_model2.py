import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
import numpy as np


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

    # Podział danych na zbiór walidacyjny
    X_train, X_val, y_train, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=42
    )

    # Inicjalizacja modelu sieci neuronowej
    model = Sequential(
        [
            Dense(128, activation="relu", input_shape=(X_train.shape[1],)),
            Dense(64, activation="relu"),
            Dense(1),  # Wyjście dla regresji
        ]
    )

    model.compile(
        optimizer=Adam(learning_rate=1e-6), loss="mse", metrics=["mse", "mae"]
    )

    # Trenowanie modelu
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=10,
        verbose=1,
    )

    # Ocena modelu
    predictions = model.predict(X_test).flatten()

    # Obliczenie MSE, RMSE i R²
    mse = mean_squared_error(y_test, predictions)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, predictions)

    print(f"  Mean Squared Error (MSE): {mse}")
    print(f"  Root Mean Squared Error (RMSE): {rmse}")
    print(f"  R-squared (R²): {r2}")

    # Zapisanie modelu do pliku
    model.save("../out/neural_network_model.h5")

    print("✅ Model sieci neuronowej wytrenowany i zapisany!")


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
