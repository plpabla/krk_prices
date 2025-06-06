import sys
import pandas as pd
import xgboost as xgb
import pickle
import optuna
from sklearn.model_selection import cross_val_score
from optuna.samplers import RandomSampler
from sklearn.metrics import median_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score


# Konwersja kolumn na kategorie
def convert_str_to_category(train: pd.DataFrame, test: pd.DataFrame, city_name="otodom") -> tuple[
    pd.DataFrame, pd.DataFrame]:
    category_mappings = {}
    for col in train.select_dtypes(include=["object"]).columns:
        train[col] = train[col].astype("category")
        category_mappings[col] = dict(enumerate(train[col].cat.categories))

    with open(f"../out/category_mappings_{city_name}.pkl", "wb") as file:
        pickle.dump(category_mappings, file)

    for col in test.select_dtypes(include=["object"]).columns:
        test[col] = test[col].astype("category")
    for col in train.select_dtypes(include=["category"]).columns:
        test[col] = test[col].cat.set_categories(train[col].cat.categories)
    for col in test.select_dtypes(include=["category"]).columns:
        train[col] = train[col].cat.set_categories(test[col].cat.categories)
    return train, test


# Funkcja celu dla Optuny
def objective(trial):
    param = {
        'max_depth': trial.suggest_int('max_depth', 3, 10),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
        'n_estimators': trial.suggest_int('n_estimators', 100, 1000),
        'subsample': trial.suggest_float('subsample', 0.5, 1.0),
        'colsample_bytree': trial.suggest_float('colsample_bytree', 0.5, 1.0),
        'min_child_weight': trial.suggest_int('min_child_weight', 1, 10),
        'gamma': trial.suggest_float('gamma', 0, 5),
    }

    model = xgb.XGBRegressor(**param,enable_categorical=True, tree_method="hist",objective="reg:squarederror", random_state=42)

    score = cross_val_score(model, X_train, y_train, cv=3, scoring="neg_median_absolute_error").mean()
    return score


# Główna funkcja
def run(filename: str = "krakow"):
    global X_train, y_train  # udostępniamy zmienne dla objective()

    # Wczytanie danych
    train_data = pd.read_csv(f"../data/{filename}_district_train.csv")
    test_data = pd.read_csv(f"../data/{filename}_district_test.csv")

    X_train = train_data.drop(columns=["price", "price_m2"])
    y_train = train_data["price"]
    X_test = test_data.drop(columns=["price", "price_m2"])
    y_test = test_data["price"]

    X_train, X_test = convert_str_to_category(X_train, X_test, city_name=filename)

    # Uruchomienie optymalizacji
    # study = optuna.create_study(study_name="xgboost_optuna_study", direction='maximize')
    study = optuna.create_study(sampler=RandomSampler(), direction="maximize")
    study.optimize(objective, n_trials=100, show_progress_bar=True, n_jobs=-1)

    best_params = study.best_params
    print(f"\n✅ Najlepsze parametry: {best_params}")

    # Trenowanie najlepszego modelu
    best_model = xgb.XGBRegressor(**best_params, enable_categorical=True,objective="reg:squarederror", random_state=42)
    best_model.fit(X_train, y_train)

    # Predykcje na zbiorze testowym
    y_pred = best_model.predict(X_test)

    # Obliczenie mediany bezwzględnego błędu
    med_abs_error = median_absolute_error(y_test, y_pred)
    print(f"Median Absolute Error na zbiorze testowym: {med_abs_error:.2f}")

    # Obliczenie błędu średniokwadratowego (MSE)
    mse = mean_squared_error(y_test, y_pred)
    rmse = mse ** 0.5
    print(f"Root Mean Squared Error (RMSE) na zbiorze testowym: {rmse:.2f}")

    r2 = r2_score(y_test, y_pred)
    print(f"R^2 na zbiorze testowym: {r2:.2f}")

    # Zapisz model
    with open(f"../out/{filename}_best_model.pkl", "wb") as file:
        pickle.dump(best_model, file)

    print("✅ Najlepszy model XGBoost został wytrenowany i zapisany!")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        run(filename)
    else:
        run()
