import socket
import os
import sys
import binascii
import re as regex

# https://regex101.com/r/2l8eJp/3

DGRAM_REGEX = regex.compile(r'(?:^([fF]{12})(([0-9a-fA-F]{12}){16})([0-9a-fA-F]{12})?$)')

def setup():
    project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "remotewol.settings")

    sys.path.append(project_path)
    os.chdir(project_path)

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()


def start():
    from webapp.models import Device, GeneralSettings

    settings = GeneralSettings.get_solo()

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((settings.listener_address, settings.listener_port))

    while True:
        data, addr = sock.recvfrom(108)
        handle_data(data)


def handle_data(data):
    packet = binascii.hexlify(data).decode('utf-8')

    if DGRAM_REGEX.match(packet):
        search = DGRAM_REGEX.search(packet)

        received_mac = search.group(3)
        received_secret = search.group(4)

        from webapp.models import Device, GeneralSettings

        # todo do something if there are no devices found
        device = Device.objects.filter(listener=True).filter(mac=received_mac)[0]

        settings = GeneralSettings.get_solo()
        if settings.enforce_secret:
            if device.secret != received_secret:
                print("The secrets do not match")
                return

        from webapp.utils import wolutils
        wolutils.forward_packet(packet, (device.target_address, device.target_port))


if __name__ == '__main__':
    setup()
    start()