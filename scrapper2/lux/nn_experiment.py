import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import median_absolute_error

import random
import numpy as np
import torch

seed = 42

random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

# 1. Wczytaj dane
df = pd.read_csv('lux_3k_district_train_predictions.csv')

# 2. Wybrane kolumny
X_raw = df[['prediction', 'luxury_level']].values.astype(np.float32)
y_raw = df['price'].values.astype(np.float32).reshape(-1, 1)

# 3. Normalizacja tylko do NN
scaler_X = MinMaxScaler()
scaler_y = MinMaxScaler()

X_scaled = scaler_X.fit_transform(X_raw)
y_scaled = scaler_y.fit_transform(y_raw)

# 4. Podział na znormalizowane dane do NN
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)

# 5. Równoległy podział danych w oryginalnej skali – tylko do RMSE XGBoost
X_train_orig, X_test_orig, y_train_orig, y_test_orig = train_test_split(X_raw, y_raw, test_size=0.2, random_state=42)

# 6. Zamiana na tensory do NN
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

# 7. Model sieci neuronowej
class PriceNN(nn.Module):
    def __init__(self):
        super(PriceNN, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(2, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1)
        )

    def forward(self, x):
        return self.net(x)

model = PriceNN()
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
epochs = 200

losses = []

# 8. Trening NN
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    output = model(X_train)
    loss = criterion(output, y_train)
    loss.backward()
    optimizer.step()
    losses.append(loss.item())

    if epoch % 20 == 0:
        model.eval()
        with torch.no_grad():
            val_preds = model(X_test)
            val_loss = criterion(val_preds, y_test)
        print(f"Epoch {epoch}, Train Loss: {loss.item():.6f}, Val Loss: {val_loss.item():.6f}")

# 9. Ewaluacja
model.eval()
with torch.no_grad():
    preds_nn = model(X_test).numpy()
    preds_nn_rescaled = scaler_y.inverse_transform(preds_nn)
    y_test_rescaled = scaler_y.inverse_transform(y_test.numpy())

# RMSE sieci neuronowej
rmse_nn = np.sqrt(mean_squared_error(y_test_rescaled, preds_nn_rescaled))

# RMSE XGBoost: oryginalna skala predykcji i cen
rmse_xgb = np.sqrt(mean_squared_error(y_test_orig, X_test_orig[:, 0].reshape(-1, 1)))

# Median Absolute Error (MAE)
mae_xgb = median_absolute_error(y_test_rescaled, X_test_orig[:, 0].reshape(-1, 1))
mae_nn = median_absolute_error(y_test_rescaled, preds_nn_rescaled)

# 10. Accuracy ±10%
margin = 0.10
relative_errors = np.abs(preds_nn_rescaled - y_test_rescaled) / y_test_rescaled
within_10_percent = (relative_errors <= margin).sum()
accuracy_10_percent = within_10_percent / len(y_test_rescaled) * 100


diff = preds_nn_rescaled.flatten() - X_test_orig[:, 0]

num_lower = np.sum(diff < 0)  # ile razy NN < XGBoost
num_higher = np.sum(diff > 0)  # ile razy NN > XGBoost
num_equal = np.sum(diff == 0)  # ile razy są równe (opcjonalnie)

error_xgb = np.abs(X_test_orig[:, 0] - y_test_rescaled.flatten())
error_nn = np.abs(preds_nn_rescaled.flatten() - y_test_rescaled.flatten())

nn_better = np.sum(error_nn < error_xgb)
xgb_better = np.sum(error_xgb < error_nn)
equal_error = np.sum(error_nn == error_xgb)

print(f"NN lepsza w {nn_better} przypadkach")
print(f"XGBoost lepsza w {xgb_better} przypadkach")
print(f"Równe błędy w {equal_error} przypadkach")

print(f"Sieć neuronowa ściąga wartość w dół w {num_lower} przypadkach.")
print(f"Sieć neuronowa podnosi wartość w górę w {num_higher} przypadkach.")
print(f"Predykcje obu modeli są równe w {num_equal} przypadkach.")

print(f"\n➡️ RMSE XGBoost prediction only: {rmse_xgb:.2f}")
print(f"➡️ RMSE with neural network (XGBoost + luxury_level): {rmse_nn:.2f}")
print(f"✅ {accuracy_10_percent:.2f}% predykcji mieści się w ±10% od rzeczywistej ceny.")
print(f"📉 Median Absolute Error (XGBoost): {mae_xgb:.2f}")
print(f"📉 Median Absolute Error (NN): {mae_nn:.2f}")

# 11. Wykres strat
plt.figure(figsize=(10, 4))
plt.plot(losses)
plt.title("Strata (Loss) podczas treningu")
plt.xlabel("Epoka")
plt.ylabel("Loss (MSE)")
plt.grid(True)
plt.show()


plt.figure(figsize=(10, 6))

# Idealna predykcja (linia przerywana)
plt.plot(y_test_rescaled, y_test_rescaled, color='red', linestyle='--', label='Idealna predykcja')

# Mini kropki: XGBoost
plt.scatter(y_test_rescaled, X_test_orig[:, 0], alpha=0.5, color='blue', s=10, label='XGBoost')

# Mini kropki: Sieć neuronowa
plt.scatter(y_test_rescaled, preds_nn_rescaled, alpha=0.5, color='green', s=10, label='XGBoost + luxury_level (NN)')

plt.xlabel('Cena rzeczywista (PLN)')
plt.ylabel('Cena przewidziana (PLN)')
plt.title('Porównanie predykcji: XGBoost vs Sieć neuronowa')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

num_samples_nn = len(preds_nn_rescaled)

print(f"Liczba próbek predykcji sieci neuronowej: {num_samples_nn}")


# 13. Błąd vs luxury_level
luxury_levels = X_test[:, 1].numpy().reshape(-1, 1)  # znormalizowany
luxury_levels_original = scaler_X.inverse_transform(np.hstack((X_test[:, 0].numpy().reshape(-1, 1), luxury_levels)))[:, 1]

absolute_errors = np.abs(preds_nn_rescaled - y_test_rescaled)

plt.figure(figsize=(10, 4))
plt.scatter(luxury_levels_original, absolute_errors, alpha=0.6)
plt.xlabel("Poziom luksusu (od ChatGPT)")
plt.ylabel("Bezwzględny błąd predykcji (PLN)")
plt.title("Błąd predykcji vs Poziom luksusu")
plt.grid(True)
plt.show()
