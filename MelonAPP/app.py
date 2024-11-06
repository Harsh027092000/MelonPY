from Melon.app import Mymelon
melon_app = Mymelon()

#views
def Default_view(request): 
    return melon_app.render_template('Welcome.html')#render template

def docs(request): 
    return melon_app.render_template('docs.html')#render template

                                        






