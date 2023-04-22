from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

# managers
from .managers import RoleManager
from .managers import UserManager

# Create your models here.
class Role(models.Model):
    role = models.CharField(max_length=30, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RoleManager()
    
    def __str__(self):
        return self.role
    
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=60, unique=True)
    id_role = models.ForeignKey(Role, related_name='user_role', on_delete=models.CASCADE, null=True, blank=True)
    USERNAME_FIELD = 'email'
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = UserManager()
    
    def __str__(self):
        return self.email