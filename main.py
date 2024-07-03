import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import math

# URL of the tracking website
url = 'https://msblive.page.link/st2tf4K1MZrDt9wr6'

# Geofenced locations with center coordinates and radius in meters
geofences = {
    "Vista 2": {"coords": (19.970960267318482, 73.78987450095731), "radius": 50},
    "Ganesh Signifia": {"coords": (19.968322923763264, 73.78851042146266), "radius": 20},
    "Kala Nagar": {"coords": (19.969045306033493, 73.78231320119166), "radius": 20},
    "Ashoka Hospital": {"coords": (19.972864309876737, 73.79179620734959), "radius": 20},
    "Parksyde": {"coords": (19.950855779864817, 73.77529111065238), "radius": 20},
    "Curry leaves Hotel": {"coords": (19.972594501465405, 73.79389503074674), "radius": 20},
    "Podar School": {"coords": (19.941514709139145, 73.755773), "radius": 50} 
}

# Set up the WebDriver
options = Options()
options.add_argument('--headless')  # Run in headless mode (optional)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)

# Haversine formula to calculate the distance between two lat/lon points
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # radius of Earth in meters
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# Function to fetch data
def fetch_data():
    script = """
    var markersData = window.markersData || [];
    var extractedData = markersData.map(function(marker) {
        return {
            lat: marker.lat ? parseFloat(marker.lat) : null,
            lng: marker.lng ? parseFloat(marker.lng) : null,
            name: marker.name || null,
            vehicalName: marker.vehicalName || null,
            vehicalSpeed: marker.vehicalSpeed || null,
            icon: marker.icon || null,
            deviceId: marker.deviceId || null,
            status: marker.status || null
        };
    });
    return extractedData;
    """
    return driver.execute_script(script)

# Function to display data
def display_data(markers_data):
    for data in markers_data:
        print(f"Latitude: {data['lat']}, Longitude: {data['lng']}")
        print(f"Name: {data['name']}")
        print(f"Vehical Name: {data['vehicalName']}")
        print(f"Vehical Speed: {data['vehicalSpeed']}")
        print(f"Icon: {data['icon']}")
        print(f"Device ID: {data['deviceId']}")
        print(f"Status: {data['status']}")
        print('-' * 40)
        
        # Check if current coordinates are within any geofence
        current_coords = (data['lat'], data['lng'])
        for location_name, geo in geofences.items():
            center_coords = geo["coords"]
            radius = geo["radius"]
            if current_coords[0] is not None and current_coords[1] is not None:
                distance = haversine(current_coords[0], current_coords[1], center_coords[0], center_coords[1])
                if distance <= radius:
                    print(f"Bus is within {location_name} geofence")
                    if location_name == "Curry leaves Hotel":
                        for _ in range(3):
                            winsound.Beep(1000, 500)  # Frequency 1000 Hz, Duration 500 ms
                    elif location_name == "Ashoka Hospital":
                        for _ in range(10):
                            winsound.Beep(1000, 100)  # Frequency 1000 Hz, Duration 500 ms
                    elif location_name == "Vista 2":
                        for _ in range(3):
                            winsound.Beep(1000, 100)  # Frequency 1000 Hz, Duration 500 ms
                    elif location_name == "Kala Nagar":
                        for _ in range(3):
                            winsound.Beep(1000, 500)  # Frequency 1000 Hz, Duration 500 ms
                    elif location_name == "Ganesh Signifia":
                        for _ in range(10):
                            winsound.Beep(1000, 100)  # Frequency 1000 Hz, Duration 500 ms
                    elif location_name == "Podar School":
                        for _ in range(3):
                            winsound.Beep(1000, 100)  # Frequency 1000 Hz, Duration 500 ms
                    else:
                        print("No match found")   
                else:
                    #winsound.Beep(1000, 500)
                    print("No match found")

# Function to compare data
def compare_data(new_data, old_data):
    return new_data != old_data

# Fetch and display data every 15 seconds
try:
    last_data = None
    while True:
        current_data = fetch_data()
        if last_data is None or compare_data(current_data, last_data):
            display_data(current_data)
            last_data = current_data
        else:
            print("No changes detected.")
        time.sleep(10)
        
        # Refresh the page to get the latest data
        driver.refresh()
        time.sleep(5)
        
except KeyboardInterrupt:
    print("Stopping updates...")

# Close the WebDriver
driver.quit()

