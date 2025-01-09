import folium
import ast
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import pandas as pd


data = pd.read_csv("github_doc/data_test.csv")
# Example NDMI value and polygon coordinates
select_input = int(input("Parcelle choisie:"))
NDMI = data.loc[select_input, "NDVI"]  # Replace with the appropriate NDMI value
parcelle_number = data.loc[select_input, "parcelle_number"]
date = data.loc[select_input, "Date"]
# Extract the coordinates from the dataframe
coordinates_str = data.loc[select_input, "polygon_coordinates"]

# Convert the string to a Python list of coordinates
coordinates = ast.literal_eval(coordinates_str)

# Center of the map (optional: use centroid of the polygon for better centering)
center_lat = sum(lat for _, lat in coordinates) / len(coordinates)
center_lon = sum(lon for lon, _ in coordinates) / len(coordinates)

# Normalize NDMI value to range between -0.8 and 0.8
norm = Normalize(vmin=-0.8, vmax=0.8)

# Create a custom colormap from red to dark blue (red -> blue)
colors = [(1, 0, 0), (0, 0, 1)]  # Red to blue
cmap = LinearSegmentedColormap.from_list("red_to_blue", colors)

# Normalize NDMI value to range from the colormap
rgba_color = cmap(norm(NDMI))
hex_color = f'#{int(rgba_color[0]*255):02x}{int(rgba_color[1]*255):02x}{int(rgba_color[2]*255):02x}'

# Create the Folium map with a satellite tile layer
m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=15,
    tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",  # Default OSM tiles
    attr="&copy; OpenStreetMap contributors",
)

# Optional: Replace with another satellite tile source (e.g., ESRI or Mapbox)
# ESRI Satellite Imagery:
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles &copy; Esri &mdash; Source: Esri, Maxar, Earthstar Geographics, and the GIS User Community",
    name="ESRI Satellite",
).add_to(m)

# Add the polygon to the map
folium.Polygon(
    locations=[(lat, lon) for lon, lat in coordinates],  # Folium uses lat-lon order
    color="black",
    weight=1,
    fill=True,
    fill_color=hex_color,
    fill_opacity=0.7,
    popup=f"NDMI: {NDMI:.2f}"
).add_to(m)

# Add layer control for tile switching
folium.LayerControl().add_to(m)

# Save the map to an HTML file or display it directly
m.save("polygon_ndmi_map.html")  # Saves the map to an HTML file

