import requests

class TickemasterAPI:
    
    def __init__(self, api_key):
        self.api_key = api_key
        
    def getEvents(self, locale, radius, keyword, lat, long):
        
        # Create the URL
        url = "https://app.ticketmaster.com/discovery/v2/events.json"
        
        params = {
            "apikey": self.api_key,
            "locale": f"{locale}-{locale}",
            "radius": radius,
            "keyword": keyword,
            "latlong": f"{lat},{long}",
            "unit": "km"
        }
        
        # Send the request
        response = requests.get(url, params=params)
        
        # Check if the request was successful
        if response.status_code != 200:
            return None
        
        # Parse the response
        data = response.json()
        
        # Extract the events
        if("_embedded" not in data):
            return None
        
        return data["_embedded"]["events"]