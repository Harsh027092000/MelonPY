from .routing import Melon_Router
import os
from .config import template_path,static_path
import json
from urllib.parse import urlparse, parse_qs
import uuid
from jinja2 import Environment, FileSystemLoader
import mimetypes

class Mymelon:
    def __init__(self):
        # Create an instance of Router
        self.router = Melon_Router()
        self.template_dir = template_path
        self.static_dir = static_path
        self.middlewares = []
        self.sessions = {}
        self.env = Environment(loader=FileSystemLoader(self.template_dir))

    def set_session(self):
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = {}
        return session_id

    def get_session(self,key):
        return self.sessions.get(key, None)
    
    def serve_static(self, path,session_id):
        """Serve static files."""
        static_file_path = os.path.join(self.static_dir, path)
        if os.path.exists(static_file_path):
            with open(static_file_path, 'rb') as file:
                mime_type, _ = mimetypes.guess_type(static_file_path)
                return file.read(),mime_type,session_id
        return None

    def render_template(self, template_name, **context):
        """Render a template with the given context using Jinja2."""
        # Use Jinja2's template loader to get the template
        template = self.env.get_template(template_name)
        # Render the template with the provided context
        return template.render(context)  
    
    def json_response(self,context):
        """Return Json."""
        json_data = json.dumps(context)
        return json_data 
    
    def html_response(self,html):
        """Return raw html"""
        return html 
    
    def add_middleware(self, middleware_func):
        """Register a middleware function."""
        self.middlewares.append(middleware_func)

    def apply_middlewares(self, request, response=None):
        """Apply all registered middleware in sequence."""
        for middleware in self.middlewares:
            response = middleware(request, response)
        return response

    def add_route(self, path, view_func):
        """Add a new route to the framework."""
        self.router.add_route(path, view_func)

    def serve(self, path,request=None):
        """Handle incoming requests."""
        # Parse the URL and extract the query parameters
        parsed_url = urlparse(path)
        query_params = parse_qs(parsed_url.query)  # Get query parameters as a dictionary
        clean_path = parsed_url.path  # Get the path without query parameters
        # Parse session ID
        cookies = getattr(request,'cookies',{})
        session_id = cookies.get("session_id")
        if not session_id or session_id not in self.sessions:
            session_id = self.set_session()
        request.sessions = self.sessions[session_id] 
        # Check for static file requests
        if path.startswith('/static/'):
            static_path = path[len('/static/'):]  # Remove '/static/' from the path
            static_response = self.serve_static(static_path,session_id)
            if static_response:
                return static_response
        # Create or update the request object
        request.path = clean_path
        request.query_params = query_params  # Include query parameters in the request     
        self.apply_middlewares(request)
        try:
            view_func, params = self.router.resolve(clean_path)
            response = view_func(request, **params)  # Pass request data to the view
            response = self.apply_middlewares(request, response)
            if isinstance(response, tuple):
                content, content_type = response
            else:
                content, content_type = response, 'text/html'
            # Set session cookie in the response
            return content, content_type, session_id
        except KeyError:
            return None

    
