from Melon.app import Mymelon
from Melon.config import middlewares_map,error_map
from http.server import BaseHTTPRequestHandler, HTTPServer
from MelonAPP.melon_urls import Paths
import datetime
melon_app = Mymelon()

#add middlewares
for i in middlewares_map:
    melon_app.add_middleware(i)
#add routes
for i in Paths:
    melon_app.add_route(i[0],i[1])  
# Add error handlers
for i in error_map:
    melon_app.router.add_error_handler(i[0],i[1])

class MyRequestHandler(BaseHTTPRequestHandler):
    def parse_cookies(self):
        """Parse the cookies sent by the client."""
        cookies = {}
        if "Cookie" in self.headers:
            cookie_header = self.headers.get("Cookie")
            for cookie in cookie_header.split("; "):
                key, value = cookie.split("=")
                cookies[key] = value               
        return cookies
    
    def do_GET(self):
        """Handle GET requests."""
        request = self
        cookies = self.parse_cookies()
        request.cookies = cookies
        response = melon_app.serve(self.path,request)
        if response:
            content, content_type, session_id = response if isinstance(response, tuple) else (response, 'text/html', None)
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            if session_id:
                self.send_header('Set-Cookie', f'session_id={session_id}; Path=/')  # Set session cookie
            self.end_headers()
            self.wfile.write(content.encode() if isinstance(content, str) else content)
        else:
            self.send_error(404)
    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers['Content-Length'])  # Get the length of the POST data
        #Filtering Post data
        post_data = self.rfile.read(content_length).decode('utf-8')  # Read the POST data
        parsed_data = dict(item.split('=') for item in post_data.split('&')) # convert Post data into dict
        for k,v in parsed_data.items(): #replace special Character from value
            if '+' in v:
               parsed_data[k] = v.replace('+',' ')

        path = self.path  # Get the request path
        request = self  # Include POST data in the request
        cookies = self.parse_cookies()
        request.cookies = cookies
        request.POST_DATA = parsed_data
        response = melon_app.serve(path, request)  # Pass the request data to the application
        if response:
            content, content_type, session_id = response if isinstance(response, tuple) else (response, 'text/html', None)
            self.send_response(200)
            if session_id:
                self.send_header('Set-Cookie', f'session_id={session_id}; Path=/')  # Set session cookie
            self.end_headers()
            self.wfile.write(content.encode() if isinstance(content, str) else content)
        else:
            self.send_error(404)        
#run server
def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=666):
    """Run the HTTP server."""
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'[{datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S')}] -- MelonPY running on PORT: {port}')
    httpd.serve_forever()

# Add this to your main check
if __name__ == "__main__":
    run()