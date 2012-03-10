import os, sys
import django.core.handlers.wsgi
from tornado import httpserver, ioloop, wsgi

from optparse import OptionParser
parser = OptionParser()

parser.add_option('--port', dest='port')

options, args = parser.parse_args()

def runserver():
    app_dir = os.path.abspath(os.path.dirname(__file__))
    sys.path.append(os.path.dirname(app_dir))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'burstolio.settings'
    application = django.core.handlers.wsgi.WSGIHandler()

    container = wsgi.WSGIContainer(application)
    server = httpserver.HTTPServer(container)
    server.listen(options.port)
    try:
        ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        sys.exit(0)

if __name__ == '__main__':
    runserver()
