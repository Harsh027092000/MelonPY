import datetime
def logging_middleware(request, response=None):
    if not response:
        """Log each request path."""
        print(f'[{datetime.datetime.now().strftime('%d/%b/%Y %H:%M:%S')}] "{request.command} {request.path}"') 
    else:
        pass
    return response
#add middleware here