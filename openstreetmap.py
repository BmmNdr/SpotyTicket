import requests

def getPlaces(place):
    url = f"https://nominatim.openstreetmap.org/search?q={place}&format=json&addressdetails=1"

    result = requests.get(url)

    return result.json()
