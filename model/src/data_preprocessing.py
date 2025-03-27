import pandas as pd
import numpy as np
import re
import ast
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from datetime import date, timedelta

# todo utworz skrypt , zeny podzielic na train & test
# Wczytaj dane z pliku CSV
data = pd.read_csv("../data/otodom.csv")

# Dodaj kolumnę z dzielnicą
data["location"] = data["location"].apply(ast.literal_eval)
data["location_district"] = data["location"].apply(
    lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None
)

# Usuń wiersze, gdzie 'location_district' jest NaN
data = data.dropna(subset=["location_district"])

# Usuń dzielnice z pojedynczym wystąpieniem
data = data[
    data.groupby("location_district")["location_district"].transform("count") > 1
]

# Podział na train i test (stratyfikacja względem dzielnicy)
train, test = train_test_split(
    data, test_size=0.2, random_state=42, stratify=data["location_district"]
)


def preprocess_data(data):
    # Usunięcie wierszy, w których w kolumnie 'name' zawarty jest ciąg 'tbs'
    data = data[~data["name"].str.contains("tbs", case=False, na=False)]

    # Usunięcie błędnych wartości w 'build_year'
    data.loc[:, "build_year"] = data["build_year"].apply(
        lambda x: np.nan if x < 1000 or x > 2030 else x
    )

    # Przetwarzanie piętra
    def process_floor(value):
        if pd.isna(value) or value.strip() == "":
            return np.nan
        if value == "cellar":
            return -1
        if value == "ground_floor":
            return 0
        match = re.search(r"\d+", value)
        return int(match.group()) if match else np.nan

    data["floor"] = data["floor"].apply(process_floor)

    # Zamiana wartości NaN w "floor" na najczęściej występującą wartość
    data.loc[:, "floor"] = data["floor"].fillna(data["floor"].mode()[0])

    # Zamiana wartości NaN w "building_floors" na najczęściej występującą wartość w danej dzielnicy
    data.loc[:, "building_floors"] = data.groupby("location_district")[
        "building_floors"
    ].transform(
        lambda x: x.fillna(
            x.mode()[0] if not x.mode().empty else data["building_floors"].mode()[0]
        )
    )

    # Przetwarzanie liczby pokoi
    data.loc[:, "rooms"] = data["rooms"].apply(
        lambda x: int(x) if str(x).isdigit() else None
    )

    # Przetwarzanie liczby pokoi
    data.loc[:, "rooms"] = data["rooms"].apply(
        lambda x: int(x) if str(x).isdigit() else None
    )

    # Wypełnianie brakujących wartości na podstawie mediany dla każdego zakresu powierzchni
    data.loc[:, "rooms"] = data.groupby(pd.cut(data["area"], bins=10), observed=True)[
        "rooms"
    ].transform("median")

    # Jeśli nadal są brakujące wartości, obliczamy średnią powierzchnię pokoju na podstawie wszystkich danych
    if data["rooms"].isna().sum() > 0:
        # Obliczamy średnią powierzchnię pokoju
        avg_room_size = data["area"].sum() / data["rooms"].sum()

        # Zastępujemy brakujące wartości na podstawie średniej powierzchni pokoju
        data.loc[:, "rooms"] = data["rooms"].fillna(
            (data["area"] / avg_room_size).round()
        )

    # Podstawowe dane dla Krakowa
    min_rent_per_m2 = 6.64
    max_rent_per_m2 = 16.96

    # Krok 1: Sprawdzanie, czy rent mieści się w przedziale 6,64 * area < rent < 16,96 * area
    data["rent"] = data.apply(
        lambda row: (
            row["rent"]
            if (
                min_rent_per_m2 * row["area"]
                < row["rent"]
                < max_rent_per_m2 * row["area"]
            )
            else 10 * row["area"]
        ),
        axis=1,
    )

    # Uzupełnianie 'build_year' z medianą dla dzielnic
    data.loc[:, "build_year"] = data["build_year"].fillna(
        data.groupby("location_district")["build_year"].transform("median")
    )
    data.loc[:, "build_year"] = data[
        "build_year"
    ].round()  # Zaokrąglanie do pełnej liczby

    # Uzupełnianie brakujących cen na podstawie ceny za m²
    grouped = (
        data.dropna(subset=["price", "area"])
        .groupby("location_district")
        .agg(total_price=("price", "sum"), total_area=("area", "sum"))
        .reset_index()
    )
    grouped["avg_price_m2"] = grouped["total_price"] / grouped["total_area"]
    data = data.merge(
        grouped[["location_district", "avg_price_m2"]],
        on="location_district",
        how="left",
    )

    data["price"] = data.apply(
        lambda row: (
            row["avg_price_m2"] * row["area"]
            if pd.isna(row["price"]) and not pd.isna(row["area"])
            else row["price"]
        ),
        axis=1,
    )

    # Dodanie kolumny price_m2
    data["price_m2"] = data["price"] / data["area"]

    # Krok 2: Usuwanie wartości odstających w kolumnie 'price_m2'
    Q1 = data["price_m2"].quantile(0.25)
    Q3 = data["price_m2"].quantile(0.75)
    IQR = Q3 - Q1

    # Odrzucenie wartości poza zakresem IQR
    data["price_m2"] = data.apply(
        lambda row: (
            np.nan
            if (row["price_m2"] < Q1 - 1.5 * IQR) or (row["price_m2"] > Q3 + 1.5 * IQR)
            else row["price_m2"]
        ),
        axis=1,
    )

    # Uzupełnianie wartości NaN dla price_m2 średnią ceną za m²
    avg_price_m2 = data["price_m2"].mean()
    data["price_m2"] = data["price_m2"].fillna(avg_price_m2)

    # Upewnij się, że kolumna 'available' jest w formacie datetime.date
    data["available"] = pd.to_datetime(data["available"], errors="coerce").dt.date

    # Uzupełnienie brakujących wartości w 'available' pierwszym dniem bieżącego roku
    data.loc[:, "available"] = data["available"].fillna(date(date.today().year, 1, 1))

    # Zamiana dat wcześniejszych niż dzisiejszy dzień na dzisiejszą datę
    # oraz dat późniejszych niż 2 lata od dzisiaj na dzisiejszą datę
    data["available"] = data["available"].apply(
        lambda x: min(max(x, date.today()), date.today() + timedelta(days=730))
    )

    # Konwersja 'available' na liczbę dni od 1 stycznia bierzącego roku
    data["available"] = (
        pd.to_datetime(data["available"], errors="coerce")
        - pd.to_datetime(date(date.today().year, 1, 1))
    ).dt.days

    # One-Hot Encoding
    data["utilities"] = data["utilities"].apply(ast.literal_eval)
    mlb = MultiLabelBinarizer()
    utilities_encoded = mlb.fit_transform(data["utilities"])
    utilities_df = pd.DataFrame(
        utilities_encoded, columns=["utilities_" + col for col in mlb.classes_]
    )
    data = data.join(utilities_df)

    categorical_features = [
        "heating",
        "state",
        "market",
        "ownership",
        "ad_type",
        "location_district",
    ]
    for feature in categorical_features:
        encoded = pd.get_dummies(data[feature], prefix=feature)
        data = data.join(encoded)
        data[encoded.columns] = data[encoded.columns].astype(int)

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
            "avg_price_m2",
            "location_district",
        ],
        inplace=True,
    )

    return data


# Przetworzenie i zapis zestawów train/test
train = preprocess_data(train)
test = preprocess_data(test)

# Porównanie kolumn i dodanie brakujących kolumn z zerami
for col in train.columns:
    if col not in test.columns:
        test[col] = 0

for col in test.columns:
    if col not in train.columns:
        train[col] = 0

# Zapewnienie, że kolumny w train i test są w tej samej kolejności
train = train[sorted(train.columns)]
test = test[sorted(test.columns)]

##todo make path operating system independent with os.path.join
train.to_csv("../data/otodom_train.csv", index=False)
test.to_csv("../data/otodom_test.csv", index=False)

print("✅ Dane przetworzone i zapisane jako train.csv oraz test.csv")
