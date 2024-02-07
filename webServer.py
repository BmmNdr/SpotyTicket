import requests
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Extract the authorization code from the query parameters
        query_components = parse_qs(urlparse(self.path).query)
        if 'code' in query_components:
            authorization_code = query_components['code'][0]
            #print(f"Authorization code received: {authorization_code}")
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization Successful</h1><p>You can close this window now.</p></body></html>')
            self.server.authorization_code = authorization_code
        else:
            #print("Authorization code not found in callback URL")
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<html><body><h1>Authorization Failed</h1><p>Authorization code not found in callback URL.</p></body></html>')
            
def run_server(port, server_class=HTTPServer, handler_class=CallbackHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    #print(f"Starting callback server on port {port}...")
    httpd.handle_request()
    return httpd.authorization_code