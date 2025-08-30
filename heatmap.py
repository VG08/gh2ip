import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the grid data
df = pd.read_csv('land_price_grid_2.csv')

# Optional: downsample if you have a very large file
# df = df.sample(20000)  # For faster plotting

# Pivot data for heatmap: row as latitude, column as longitude, values as price
heatmap_data = df.pivot_table(
    index='Latitude', 
    columns='Longitude', 
    values='Land_Price_lakhs_per_acre'
)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlOrRd', cbar_kws={'label': 'Land Price per Acre (Lakhs)'})

plt.title('Imaginary Gujarat Land Price Heatmap (per acre, in lakhs)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.tight_layout()
plt.show()