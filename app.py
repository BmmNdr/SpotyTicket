from SpotifyAPI import SpotifyAPI 
from TicketmasterAPI import TickemasterAPI
import openstreetmap
import secret

def getArtistsNames(spoty):   
    names = []
    
    if(spoty.access_token):
        artists = spoty.getFollowedArtists()
        
        for artist in artists:
            names.append(artist['name'])
    
    return names

def getLocation():
    
    print("Dove vuoi cercare l'evento?")
    
    place = None
    
    nomeTappa = input("Inserisci il nome della città: ")
    places = openstreetmap.getPlaces(nomeTappa)
    
    while(place == None):
        if(places.__len__() <= 0):
            print("Nessuna città trovata, riprovare\n")
            numero = -1
        else:
            if(places.__len__() > 1):
                j = 1
                for place in places:
                    print(str(j) + " " + place["display_name"] + " - " + place["addresstype"])
                    j += 1

                numero = '-1'
                while( not numero.isnumeric() or not (int(numero) > 0 and int(numero) <= j)):
                    numero = input("Inserire il numero della città corretta: ")
            else:
                numero = 1   
                
        place = places[int(numero)-1] if int(numero) >= 0 else None
        
    return place

if __name__ == '__main__':
    print("Benvenuto")
    
    spoty = SpotifyAPI(secret.getClientID(), secret.getClientSecret(), 'user-follow-read', 8888)
    artists = getArtistsNames(spoty)
    
    location = getLocation()
    
    ticketmaster = TickemasterAPI(secret.getTicketmasterKey())
    
    radius = '-1'
    while(not radius.isnumeric() or not (int(radius) > 0 and int(radius) < 20000)):
        radius = input("Inserire il raggio in cui cercare: ")
        
    locale = location['address']['country_code']
    
    artists_events = {}
    
    for artist in artists:
        events = ticketmaster.getEvents(locale, int(radius), artist, location['lat'], location['lon'])
        if(events):
            print(f"Evento per {artist}: " + events[0]['url'])
            artists_events[artist] = events
    
    print("Grazie per aver usato il nostro servizio")
    
    #all'interno di artists_events ci sono tutti gli eventi vicini per ogni artista, quindi si possono esplorare altre servizi
    