from SpotifyAPI import SpotifyAPI 
import secret

if __name__ == '__main__':
    print("Benvenuto")
    
    spoty = SpotifyAPI(secret.getClientID(), secret.getClientSecret(), 'user-follow-read', 8888)
    
    if(spoty.access_token):
        print("Autorizzazione riuscita")
        
        artists = spoty.getFollowedArtists()      