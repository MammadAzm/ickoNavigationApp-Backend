from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(EnumerationType)
admin.site.register(Enumeration)
admin.site.register(Target)
admin.site.register(GPSData)
admin.site.register(StatusData)
