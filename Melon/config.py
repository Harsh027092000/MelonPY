import os
from Melon.error import not_found_view,internal_error_view
from .middleware import logging_middleware

#templates DIR
template_path = os.path.join(os.path.dirname(__file__), 'melon_templates')

#static DIR
static_path = os.path.join(os.path.dirname(__file__), 'static')

#under testing 
#register error handler
error_map = [
    (404,not_found_view),
    (500,internal_error_view),
]

#register middleware
middlewares_map = [
    logging_middleware,
]