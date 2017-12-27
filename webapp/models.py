from django.db import models
from django.urls import reverse

from macaddress.fields import MACAddressField


class Device(models.Model):
    name = models.CharField(max_length=100, default='Computer')
    mac = MACAddressField(default='00:12:3c:37:64:8f')
    secret = models.CharField(max_length=12, default='0a1b3c4d5e6f')
    description = models.TextField(default='This is a dank-ass description for a dank-af device')
    target_address = models.GenericIPAddressField(default="255.255.255.255")
    target_port = models.SmallIntegerField(default=9)
    listener = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('webapp:update-device', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Global(models.Model):
    listener_address = models.GenericIPAddressField()
    listener_port = models.SmallIntegerField()
    sent_packets = models.SmallIntegerField()
