import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.colors as colors

# Load the data
data = pd.read_csv("../../data/otodom.csv")
bg = "./krk.png"
bg_coord = [(50.144579, 19.757886), (49.972568, 20.120011)]

# Calculate price per square meter
data["price_per_sqm"] = data["price"] / data["area"]

# Create the figure and plot
fig, ax = plt.subplots(figsize=(12, 8))

# Load and display the background image
bg_img = mpimg.imread(bg)
ax.imshow(
    bg_img, extent=[bg_coord[0][1], bg_coord[1][1], bg_coord[1][0], bg_coord[0][0]]
)

# Set color normalization with thresholds
norm = colors.Normalize(
    vmin=10000, vmax=30000
)  # Adjust these values based on your data

scatter = ax.scatter(
    data["location_lon"],
    data["location_lat"],
    c=data["price_per_sqm"],
    cmap="hot_r",
    s=30,  # marker size
    alpha=0.75,  # transparency
    norm=norm,  # Apply the normalization
)

# Keep original aspect ratio
ax.axis("equal")

# Add a colorbar
plt.colorbar(scatter, label="Price per square meter")

# Customize the plot
ax.set_title("Real Estate Prices per Square Meter by Location")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Add grid for better readability
ax.grid(True, alpha=0.3)

# Enable tight layout
plt.tight_layout()

# Show the plot and block until window is closed
plt.show(block=True)
