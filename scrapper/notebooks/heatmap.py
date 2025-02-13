import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors
import numpy as np
from scipy.stats import gaussian_kde

# Load the data
data = pd.read_csv("../../otodom.csv")
bg = "./krk.png"
bg_coord = [(50.144579, 19.757886), (49.972568, 20.120011)]

# drop offers without a price or area
data.dropna(subset=["price", "area"], inplace=True)

# Calculate price per square meter
data["price_per_sqm"] = data["price"] / data["area"]
# data["price_per_sqm"] = data["price_per_sqm"].clip(25000, 30000)

# Clean the data by removing NaN and infinite values
data = data.replace([np.inf, -np.inf], np.nan)
data = data.dropna(subset=["price_per_sqm", "location_lon", "location_lat"])

# Create the figure and plot
fig, ax = plt.subplots(figsize=(12, 8))

# Load and display the background image
bg_img = mpimg.imread(bg)
ax.imshow(
    bg_img, extent=[bg_coord[0][1], bg_coord[1][1], bg_coord[1][0], bg_coord[0][0]]
)

# Create a grid of points
POINTS = 200
x_min, x_max = bg_coord[0][1], bg_coord[1][1]
y_min, y_max = bg_coord[1][0], bg_coord[0][0]
x_grid, y_grid = np.mgrid[x_min : x_max : POINTS * 1j, y_min : y_max : POINTS * 1j]

# Stack coordinates into pairs
positions = np.vstack([x_grid.ravel(), y_grid.ravel()])

# Create kernel density estimate
values = np.vstack([data["location_lon"], data["location_lat"]])
kernel = gaussian_kde(values, weights=data["price_per_sqm"].values)

# Evaluate kernel on grid
z = kernel(positions).reshape(POINTS, POINTS)

# Plot heatmap
heatmap = ax.imshow(
    z.T, extent=[x_min, x_max, y_min, y_max], origin="lower", cmap="hot_r", alpha=0.7
)
# colormaps: RdYlGn_r, hot_r

# Add a colorbar
# plt.colorbar(heatmap, label="Price Density per Square Meter")

# Customize the plot
ax.set_title("Real Estate Price Density per Square Meter")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Add grid for better readability
ax.grid(True, alpha=0.3)

# Enable tight layout
plt.tight_layout()

# Show the plot and block until window is closed
plt.show(block=True)
