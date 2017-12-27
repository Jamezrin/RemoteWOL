from django.contrib import admin
from solo.admin import SingletonModelAdmin

from webapp.models import Device, GeneralSettings


admin.site.register(GeneralSettings, SingletonModelAdmin)
admin.site.register(Device)

