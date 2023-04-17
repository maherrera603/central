from django.contrib import admin
#models
from .models import Pattient, Family

# Register your models here.
admin.site.register(Pattient)
admin.site.register(Family)
