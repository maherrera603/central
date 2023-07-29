from django.db import models

# models
from applications.employees.models import Employee

# managers
from .managers import StatusManager
from .managers import SpecialityManager
from .managers import DoctorManager


# Create your models here.
class Status(models.Model):
    status = models.CharField(max_length=70, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = StatusManager()
    
    def __str__(self):
        return self.status
    
    
class Speciality(models.Model):
    speciality = models.CharField(max_length=70, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = SpecialityManager()
    
    def __str__(self):
        return self.speciality
    
    
class Doctor(models.Model):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    type_document = models.CharField(max_length=30)
    document = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10)
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = DoctorManager()
    
    def __str__(self):
        return self.name