from django.db import models
# models
from applications.administrations.models import Status, Speciality, Doctor
from applications.pattients.models import Pattient
# managers
from .managers import CiteManager


# Create your models here.
class Cites(models.Model):
    name = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    type_document = models.CharField(max_length=30)
    document = models.CharField(max_length=20, unique=True)
    phone = models.CharField(max_length=10, blank=True)
    eps = models.CharField(max_length=50, blank=True)
    id_speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE)
    id_doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True)
    id_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    date_cite = models.DateField(blank=True, null=True)
    hour_cite = models.TimeField(blank=True, null=True)
    id_pattient = models.ForeignKey(Pattient, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = CiteManager()
    
    def __str__(self):
        return self.name