'''
This is webserver based on CherryPy framework. This server is used to replace
the built-in django development runserver in production environment.
It is also capable of servering static files, uncommend the line
    # self.mount_static(settings.STATIC_URL, BASE_DIR2)
to make this CherryPy server serve static files.
'''

import os
from pathlib import Path
import cherrypy
import django
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler

# tells Django where to find your settings file
os.environ["DJANGO_SETTINGS_MODULE"] = 'configs.settings'

# initializes Django and loads the settings specified by DJANGO_SETTINGS_MODULE
django.setup()

# run server using CherryPy as web server
class DjangoApplication(object):
    HOST = "0.0.0.0"
    PORT = 8000

    def run(self):
        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            # 'server.ssl_module': 'builtin',
            # 'server.ssl_certificate': os.path.join(BASE_DIR2, 'ssl_cert.pem'),
            # 'server.ssl_private_key': os.path.join(tdir, 'ssl_key.pem'),
            'engine.autoreload_on': True,
            'log.screen': True,
        })
        # uncomment to call static files mount function and serve static file via cerrypy
        # self.mount_static(settings.STATIC_URL, BASE_DIR2)

        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()
        cherrypy.engine.block()

if __name__ == "__main__":
    DjangoApplication().run()

'''
you can also use cherrypy to server static files, param url: Relative url, param root: Path to static files root
but in our case, we are using WhiteNoise middleware to server static files instead

    def mount_static(self, url, root):
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.root': root,
            'tools.staticdir.dir': 'static',
            'tools.expires.on': True,
            'tools.expires.secs': 86400,
            'tools.staticdir.debug': True,
        }
        cherrypy.tree.mount(None, url, {'/': config})
'''
