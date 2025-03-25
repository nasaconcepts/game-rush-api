import json
import random
import os
import requests
from geopy.distance import geodesic
import googlemaps
import uuid

# Load the major cities data from JSON file
path = os.getcwd()
json_file_path = os.path.join(os.path.dirname(__file__), "major_cities.json")
with open(json_file_path, "r") as file:
    cities = json.load(file)



# Google Roads API key (Replace with your own key)

api_key= os.getenv("GOOGLE_MAP_API")
stree_view_url = os.getenv("STREET_VIEW_URL")
google_snap_to_road= os.getenv("GOOGLE_SNAP_TO_ROAD_URL")

def get_random_coordinates():
    """Pick a random city and generate nearby coordinates"""
    city = random.choice(cities)
    print(f"City picked =>{city}")
    base_lat = city["latitude"]
    base_lng = city["longitude"]

    # Generate a random offset (±0.1 degrees ~ 11km variation)
    lat_offset = random.uniform(-0.1, 0.1)
    lng_offset = random.uniform(-0.1, 0.1)

    return base_lat + lat_offset, base_lng + lng_offset
def check_street_view(lat,lon):
    try:
        url = f"{stree_view_url}{lat},{lon}&key={api_key}"
        response = requests.get(url).json()

        if response["status"] == "OK":
            return True  # Street View is available
        else:
            return False  # No Street View at this location


    except Exception as ex:
        print(f"Error calling street view api {ex}")

def snap_to_road(lat, lng):
    """Use Google Roads API to find the nearest road"""
    url = f"{google_snap_to_road}{lat},{lng}&key={api_key}"
    response = requests.get(url)
    data = response.json()

    if "snappedPoints" in data:
        snapped_location = data["snappedPoints"][0]["location"]
        return snapped_location["latitude"], snapped_location["longitude"]
    else:
        default_city= random.choice(cities)
        return default_city["latitude"], default_city["longitude"]
def get_city_name(latitude,longitude):
    gmaps = googlemaps.Client(key=f"{api_key}")

    # Reverse geocode the coordinates
    result = gmaps.reverse_geocode((latitude, longitude))
   

    if result:
        for component in result[0]['address_components']:
            if "locality" in component['types']:  # City name
                return component['long_name']

    return "Unknown"

def get_valid_location(retries=5):
    print(f"Retry Count =>{retries}")
    if retries == 0:
        return None  # Fallback if no valid city found

    random_lat, random_lng = get_random_coordinates()
    snapped_coordinates = snap_to_road(random_lat, random_lng)
    city_name = get_city_name(snapped_coordinates[0], snapped_coordinates[1])

    if city_name.lower() == "unknown" or not check_street_view(snapped_coordinates[0], snapped_coordinates[1]):
        return get_valid_location(retries - 1)

    return {
        "locationId": str(uuid.uuid4()),
        "cityName": city_name,
        "latitude": snapped_coordinates[0],
        "longitude": snapped_coordinates[1]
    }



def generate_random_valid_location(locationCounts=5):
    targetLocations = []
    for i in range(locationCounts):
        # retries = 5
        targetLocations.append(get_valid_location())

    return targetLocations

def calculate_distance_between_coordinates_km(guessedLocation, targetLocation):
    """Calculate the distance between two coordinates in kilometers"""
    # Define two coordinates (latitude, longitude)
    coord1 = (guessedLocation["latitude"], guessedLocation["longitude"])
    coord2 = (targetLocation["latitude"] ,targetLocation["longitude"])

    # Calculate distance in kilometers
    distance_km = geodesic(coord1, coord2).kilometers
    print(f"Distance: {distance_km:.2f} km")
    return round(distance_km,2)


