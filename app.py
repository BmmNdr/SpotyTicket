from SpotifyAPI import SpotifyAPI 
import openstreetmap
import secret

def getArtistsNames():
    spoty = SpotifyAPI(secret.getClientID(), secret.getClientSecret(), 'user-follow-read', 8888)
    
    names = []
    
    if(spoty.access_token):
        artists = spoty.getFollowedArtists()
        
        for artist in artists:
            names.append(artist['name'])
    
    return names

def getLocation():
    
    print("Inserisci il nome della città: ")
    
    place = None
    
    nomeTappa = input("Dove vuoi cercare l'evento?")
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
    
    #artists = getArtistsNames()
    
    #location = getLocation()
    
    