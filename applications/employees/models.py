from django.db import models
# models
from applications.users.models import User
# managers
from .managers import EmployeeManager


# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    type_document = models.CharField(max_length=50)
    document = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10)
    id_user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()
    
    def __str__(self):
        return f"{self.name} {self.lastname}"
    