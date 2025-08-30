import numpy as np
import pandas as pd

# Define latitude and longitude ranges
lat_min, lat_max = 20.5, 30.74
lon_min, lon_max = 75.75, 79.5

n_grids = 10000
n_rows = int(np.sqrt(n_grids))
n_cols = int(np.sqrt(n_grids))

# Create mesh grid
latitudes = np.linspace(lat_min, lat_max, n_rows)
longitudes = np.linspace(lon_min, lon_max, n_cols)
lats, lons = np.meshgrid(latitudes, longitudes)

# Flatten grid
lats_flat = lats.flatten()
lons_flat = lons.flatten()

# Assign random values between 55 and 95
prices = np.random.uniform(0,1, n_grids)

# Create DataFrame
grid_df = pd.DataFrame({
    'Latitude': lats_flat,
    'Longitude': lons_flat,
    'Land_Price_lakhs_per_acre': prices
})

# Save as CSV
grid_df.to_csv('land_price_grid_2.csv', index=False)
grid_df.head()
