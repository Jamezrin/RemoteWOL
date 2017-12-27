from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.views.generic import View, ListView, DetailView
from solo.models import SingletonModel

from webapp.utils import wolutils

from webapp import urls
from webapp.models import Device, GeneralSettings


class ListDevices(LoginRequiredMixin, ListView):
    template_name = 'devices.html'
    model = Device

    def get_queryset(self):
        return Device.objects.all()


class CreateDevice(LoginRequiredMixin, CreateView):
    template_name = 'device_form.html'
    model = Device
    fields = ['name', 'mac', 'secret', 'description', 'target_address', 'target_port', 'listener']


class UpdateDevice(LoginRequiredMixin, UpdateView):
    template_name = 'device_form.html'
    model = Device
    fields = ['name', 'mac', 'secret', 'description', 'target_address', 'target_port', 'listener']


class UpdateSettings(LoginRequiredMixin, UpdateView):
    template_name = 'settings_form.html'
    model = GeneralSettings
    fields = ['listener_address', 'listener_port', 'packet_count']

    def get_object(self, queryset=None):
        return GeneralSettings.get_solo()


@login_required
def delete_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    print("Deleted device: " + str(device))
    device.delete()
    return redirect('webapp:home')


@login_required
def wake_device(request, device_id):
    device = get_object_or_404(Device, pk=device_id)
    print("Waking up device: " + str(device))
    wolutils.wake_device(device, GeneralSettings.get_solo().packet_count)

    return redirect('webapp:home')


@login_required
def temp(request):
    return HttpResponse('This is just a temporary placeholder for logged in users')