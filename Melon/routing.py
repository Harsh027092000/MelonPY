import re

class Melon_Router:
    def __init__(self):
        self.routes = {}
        self.error_handlers = {}

    def add_route(self, path, view_func):
        """Add a route by associating a path with a view function."""
        # Convert dynamic parts <param> to regex (e.g., '/user/<id>' becomes '/user/(?P<id>\w+)')
        path = re.sub(r'<(\w+)>', r'(?P<\1>\\w+)', path)
        path = f'^{path}$'
        self.routes[path] = view_func

    def add_error_handler(self, error_code, view_func):
        """Add a custom error handler for a specific error code."""
        self.error_handlers[error_code] = view_func    

    def resolve(self, path):
        """Find and return the view function for the given path."""
        for route, view_func in self.routes.items():
            match = re.match(route, path)
            if match:
                # Return the view function and the matched parameters as a dictionary
                return view_func, match.groupdict()
        return self.default_response, {}

    def default_response(self, request):
        """Return a default response for routes not found."""
        return f"404 Not Found: {request.path}"
    
    def handle_error(self, error_code):
        """Handle errors by returning the appropriate error handler."""
        if error_code in self.error_handlers:
            return self.error_handlers[error_code]({})
        return f"500 Internal Server Error"