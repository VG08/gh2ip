import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
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


# 1. Create the FastAPI app instance
app = FastAPI()

# 2. Mount the 'static' directory to serve static files like CSS and JS
# The 'name="static"' part is important for the templating
app.mount("/static", StaticFiles(directory="static"), name="static")

# 3. Point to the 'templates' directory for your Jinja2 templates
templates = Jinja2Templates(directory="templates")

# 4. Define the data to be passed to the template
# In a real app, this would come from a database, an API, etc.
with open("renewable_power_plants_india_large.json", "r") as f:
    plants = json.load(f)

template_data = {
    "layers": [
        {"id": "existingAssets", "name": "Existing & Planned Assets", "checked": True},
        {"id": "renewableSources", "name": "Renewable Energy Sources", "checked": True},
        {"id": "demandCenters", "name": "Demand Centers", "checked": True},
        {"id": "transportLogistics", "name": "Transport Logistics", "checked": True},
        {"id":"landPrice", "name": "Land Prices", "checked":True}
    ],
    "optimisation_params": [
        {"id": "proximityRenewable", "name": "Proximity to Renewables", "value": 70},
        {"id": "marketDemand", "name": "Market Demand", "value": 80},
        {"id": "costOpt", "name": "Cost Optimisation", "value": 90}
    ],
    "map_data": {
        "assets": [
            # {"id": 1, "type": "Plant", "status": "Existing", "name": "Reliance Jamnagar Complex", "lat": 22.3733, "lng": 70.0577, "capacity": 500},
            # {"id": 2, "type": "Storage", "status": "Planned", "name": "Adani Mundra Solar Park Storage", "lat": 22.84, "lng": 69.71, "capacity": 200},
            # {"id": 3, "type": "Plant", "status": "Planned", "name": "ACME Solar Plant, Rajasthan", "lat": 26.9124, "lng": 75.7873, "capacity": 350}
        ],
        "renewables": [
            {"id": 1, "type": "Solar", "name": "Bhadla Solar Park", "lat": 27.5333, "lng": 71.9167, "potential": 2245},
            {"id": 2, "type": "Wind", "name": "Muppandal Wind Farm", "lat": 8.2718, "lng": 77.5358, "potential": 1500}
        ],
        "demand": [
            {"id": 1, "name": "Industrial Hub - Gujarat", "lat": 23.0225, "lng": 72.5714, "demand": "High"},
            {"id": 2, "name": "Transport Corridor - Delhi", "lat": 28.7041, "lng": 77.1025, "demand": "Low"}
        ],
        "transport": {
            "type": "FeatureCollection",
            "features": [{
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[70.0577, 22.3733], [72.5714, 23.0225]]}
            }]
        },
        "optimisedLocations": [
            {"lat": 25.4358, "lng": 81.8463, "score": 95, "reason": "High solar potential, proximity to industrial demand."},
            {"lat": 17.3850, "lng": 78.4867, "score": 88, "reason": "Balanced renewable access and emerging tech hub demand."}
        ]
    }
}

for i, plant in enumerate(plants):
    template_data["map_data"]["renewables"].append({"id": i, **plant })
print(template_data["map_data"]["renewables"])
# 5. Define the main route for your application
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    # Prepare the context dictionary to pass to the template
    context = {
        "request": request, # This is required by Jinja2Templates
        "template_data": template_data,
        # IMPORTANT: Unlike Flask, FastAPI+Jinja2 doesn't have a built-in 'tojson' filter.
        # We convert the map_data to a JSON string here in Python...
        "map_data_json": json.dumps(template_data["map_data"])
    }
    return templates.TemplateResponse("index.html", context)



@app.get("/landprices")
async def land_prices():
    return data_list