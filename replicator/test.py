# This is so models get loaded.
import socket

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from webapp.models import Device, GeneralSettings

def start():
    print("Starting the listener...")




if __name__ == '__main__':
    start()
