import requests
import folium
import geocoder
import webbrowser

g = geocoder.ip('me')

if g.ok:
    location = g
else:
    print("Unable to determine location.")
    exit()

Latitude = location.lat
Longitude = location.lng

API_KEY = 'v_r1E2cUOFDJwKq6hIZZWoPo85rTCyMeuNGDmzdXT58'  
GEOCODE_URL = 'https://geocode.search.hereapi.com/v1/geocode'
BASE_URL = 'https://router.hereapi.com/v8/routes'

inp_location1 = input("Location of starting point: ")
inp_location2 = input("Location of ending point: ")

def geocode(location):
    params = {
        'q': location,
        'apiKey': API_KEY
    }
    response = requests.get(GEOCODE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['items']:
            return data['items'][0]['position']
    return None

location1 = geocode(inp_location1)
location2 = geocode(inp_location2)

if location1 and location2:
    lat_1 = location1['lat']
    long_1 = location1['lng']
    lat_2 = location2['lat']
    long_2 = location2['lng']
    
    print("Starting Location:", lat_1, long_1)
    print("Ending Location:", lat_2, long_2)
else:
    print("One or both locations not found.")
    exit()

start = f"{lat_1},{long_1}"
end = f"{lat_2},{long_2}"

url = f"{BASE_URL}?transportMode=car&origin={start}&destination={end}&return=summary"

params = {
    'apikey': API_KEY
}

start = f"{lat_1},{long_1}"
end = f"{lat_2},{long_2}"

url = f"{BASE_URL}?transportMode=car&origin={start}&destination={end}&return=summary"

params = {
    'apikey': API_KEY
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()

    if 'routes' in data and len(data['routes']) > 0:
        print("Route found.")
        
        m = folium.Map(location=[Latitude, Longitude], zoom_start=10)

        folium.Marker(location=[float(lat_1), float(long_1)], popup='Starting Location', icon=folium.Icon(color='green')).add_to(m)
        folium.Marker(location=[float(lat_2), float(long_2)], popup='Ending Location', icon=folium.Icon(color='red')).add_to(m)

        m.save('TrackingDrone.html')
        print("Map has been created and saved as 'TrackingDrone.html'.")
        webbrowser.open("TrackingDrone.html")
    else:
        print("No routes found for the given locations.")
else:
    print(f"Error: {response.status_code} - {response.text}")
