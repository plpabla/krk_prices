import pandas as pd
import torch
import torch.nn as nn
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 1. Wczytaj dane
df = pd.read_csv('lux_district_train_predictions.csv')

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
torch.manual_seed(42)

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

# 10. Accuracy ±10%
margin = 0.10
relative_errors = np.abs(preds_nn_rescaled - y_test_rescaled) / y_test_rescaled
within_10_percent = (relative_errors <= margin).sum()
accuracy_10_percent = within_10_percent / len(y_test_rescaled) * 100

print(f"\n➡️ RMSE XGBoost prediction only: {rmse_xgb:.2f}")
print(f"➡️ RMSE with neural network (XGBoost + luxury_level): {rmse_nn:.2f}")
print(f"✅ {accuracy_10_percent:.2f}% predykcji mieści się w ±10% od rzeczywistej ceny.")

# 11. Wykres strat
plt.figure(figsize=(10, 4))
plt.plot(losses)
plt.title("Strata (Loss) podczas treningu")
plt.xlabel("Epoka")
plt.ylabel("Loss (MSE)")
plt.grid(True)
plt.show()

# 12. Porównanie predykcji – wykres
plt.figure(figsize=(10, 6))
plt.plot(y_test_rescaled, y_test_rescaled, color='red', linestyle='--', label='Idealna predykcja')
plt.scatter(y_test_rescaled, X_test_orig[:, 0], alpha=0.5, color='blue', label='XGBoost')
plt.scatter(y_test_rescaled, preds_nn_rescaled, alpha=0.5, color='green', label='XGBoost + luxury_level (NN)')
plt.xlabel('Cena rzeczywista (PLN)')
plt.ylabel('Cena przewidziana (PLN)')
plt.title('Porównanie predykcji: XGBoost vs Sieć neuronowa')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

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
