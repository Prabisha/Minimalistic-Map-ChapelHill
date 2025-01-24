import matplotlib.pyplot as plt
import osmnx as ox
from geopy.geocoders import Nominatim
from shapely.geometry import Point

# Define city name and buffer distance
city_name = "Chapel Hill, USA"
buffer = 5000  # Buffer distance in meters

# Geolocate the city to get its latitude and longitude
geolocator = Nominatim(user_agent="OSM_map")
location = geolocator.geocode(city_name)
if not location:
    raise ValueError(f"Could not geocode {city_name}")

# Get the latitude and longitude of the city center
city_coords = (location.latitude, location.longitude)

# Download street network around the city center with a buffer distance
graph = ox.graph_from_point(city_coords, dist=buffer, network_type="all", simplify=True)

# Convert the graph to GeoDataFrame for visualization
edges = ox.graph_to_gdfs(graph, nodes=False, edges=True)

# Create a circular mask
center = Point(city_coords[1], city_coords[0])  # Longitude, Latitude as Point
circle_mask = center.buffer(buffer / 111000)  # Convert buffer from meters to degrees (~111,000 meters per degree)

# Filter edges to only include those within the circle
edges = edges[edges.intersects(circle_mask)]

# Plot the street network with a dark grey background and white streets
fig, ax = plt.subplots(figsize=(10, 10), facecolor="#62C6F2")
ax.set_facecolor("#62C6F2")  # Set background color

# Plot streets
edges.plot(ax=ax, linewidth=0.5, color="white")

# Add the circular mask
circle = plt.Circle((city_coords[1], city_coords[0]), buffer / 111000, color="#62C6F2", transform=ax.transData)
ax.add_artist(circle)

# Remove axes and set the title
ax.set_title(f"Minimalistic Map of {city_name}", fontsize=14, color="white")
ax.set_axis_off()

# Show the plot
plt.show()