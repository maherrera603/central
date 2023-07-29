from django.contrib import admin
from .models import Role, User

# Register your models here.
class RoleAdmin(admin.ModelAdmin):
    list_display = ["id", "role"]
    ordering = ["id"]

admin.site.register(Role, RoleAdmin)
admin.site.register(User)