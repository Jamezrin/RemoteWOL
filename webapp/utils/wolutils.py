import binascii
import socket

from macaddress import format_mac
from netaddr import mac_bare


def wake_device(device, times=1):
    bare_mac = format_mac(device.mac, mac_bare)
    packet = binascii.unhexlify('f' * 12 + (bare_mac * 16) + device.secret)

    for _ in range(times):
        forward_packet(packet, (device.target_address, device.target_port))


def forward_packet(packet, address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.connect(address)
    sock.send(packet)
    sock.close()
