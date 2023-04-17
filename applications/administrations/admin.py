from django.contrib import admin
# models
from .models import Status, Speciality, Doctor

# Register your models here.
admin.site.register(Status)
admin.site.register(Speciality)
admin.site.register(Doctor)
