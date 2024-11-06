#error handlings
def not_found_view(request):
    return "404 Not Found"

def internal_error_view(request):
    return "500 Internal Server Error"