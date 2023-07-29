from django.contrib import admin
# models
from .models import Status, Speciality, Doctor

# Register your models here.
class StatusAdmin(admin.ModelAdmin):
    list_display = ("id","status")
    ordering = ("id",)
    

class SpecialityAdmin(admin.ModelAdmin):
    list_display = ["id", "speciality"]
    ordering = ["id"]

class DoctorAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    ordering = ["id"]

admin.site.register(Status, StatusAdmin)
admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Doctor, DoctorAdmin)
