import csv

# File name
filename = "land_price_grid_2.csv"

# List to store all rows
data_list = []

# Open and read the CSV
with open(filename, mode="r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)  # Skip header row
    
    for row in reader:
        # Convert numeric values if needed
        latitude = float(row[0])
        longitude = float(row[1])
        land_price = float(row[2])
        
        data_list.append([latitude, longitude, land_price])

# Example: print first 5 entries
print(data_list)
