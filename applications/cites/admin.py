from django.contrib import admin
# models
from .models import Cites 
# Register your models here.

class CiteAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = ["id", "name", "last_name", "status"]
    
    
admin.site.register(Cites, CiteAdmin)