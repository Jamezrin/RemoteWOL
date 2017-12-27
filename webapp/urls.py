from django.contrib import admin
from django.urls import path

from django.contrib.auth import views as auth_views
from webapp import views as our_views

app_name = "webapp"

urlpatterns = [
    path('', our_views.ListDevices.as_view(), name='home'),

    path('device/create/', our_views.CreateDevice.as_view(), name='create-device'),
    path('device/<int:pk>/', our_views.UpdateDevice.as_view(), name='update-device'),

    path('login/', auth_views.login, {'template_name': 'login.html'}, name='login'),
    path('logout/', auth_views.logout, {'next_page': '/'}, name='logout'),

    path('device/<int:device_id>/delete', our_views.delete_device, name='delete-device'),
    path('device/<int:device_id>/wake/', our_views.wake_device, name='wake-device'),
]
