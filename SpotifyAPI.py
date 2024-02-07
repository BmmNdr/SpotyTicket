import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
import webServer

class SpotifyAPI:
    def __init__(self, client_id, client_secret, scopes, callBackPort):
        self.scopes = scopes
        self.client_id = client_id
        self.client_secret = client_secret
        
        authorization_code = self.__get_auth_token(callBackPort)
        
        self.access_token = self.__get_access_token(authorization_code, callBackPort) if authorization_code else None
        
    def __get_auth_token(self, callBackPort):
        auth_params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': f'http://localhost:{callBackPort}/callback',
            'scope': self.scopes
        }

        # Construct the authorization URL
        auth_url = 'https://accounts.spotify.com/authorize?' + urlencode(auth_params)

        webbrowser.open(auth_url)
        
        return webServer.run_server(callBackPort)

    # Function to get access token from Spotify using authorization code flow
    def __get_access_token(self, code, callBackPort):
        # Spotify token endpoint
        token_url = 'https://accounts.spotify.com/api/token'
        
        # Request body
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": f'http://localhost:{callBackPort}/callback',
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        
        # Make request to get token
        r = requests.post(token_url, data=token_data)
        if r.status_code not in range(200, 299):
            print("Failed to get token")
            return None
        
        # Extract token from response
        token_response_data = r.json()
        return token_response_data['access_token']
    
    def getFollowedArtists(self):
        # Get followed artists
            endpoint = "https://api.spotify.com/v1/me/following"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            after = None
            isFirst = True
            
            params = {
                    "limit": 50,
                    "type": "artist",
                    "after": after,
            }
            
            followed_artists = []
            
            while isFirst or after != None:
                
                params['after'] = after
                isFirst = False
                
                r = requests.get(endpoint, params=params, headers=headers)
                
                if r.status_code in range(200, 299):
                    partial_followed_artists = r.json()
                    
                    followed_artists.extend(partial_followed_artists['artists']['items'])
                        
                    after = partial_followed_artists['artists']['items'][-1]['id'] if len(partial_followed_artists['artists']['items']) == 50 else None
                else:
                    after = None
                
            return followed_artists