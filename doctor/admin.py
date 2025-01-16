from django.contrib import admin
from . models import *


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialization', 'image')
    search_fields = ('name', 'specialization')

admin.site.register(Doctor, DoctorAdmin)

