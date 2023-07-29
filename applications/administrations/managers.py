from django.db.models import Manager
from django.db.models import Q


class StatusManager(Manager):
    def get_status(self, status:int):
        try:
            return self.get(pk=status)
        except self.model.DoesNotExist:
            return False
        
    def get_all_status(self):
        return self.all()
    
    def create_status(self, data):
        status = self.model()
        status.status = data["status"]
        return status
    
    def updated_status(self, status, data):
        status = self.get(status__icontains=status)
        status.status = data["status"]
        return status


class SpecialityManager(Manager):
    def get_all_specialities(self):
        return self.all()
    
    def get_speciality_by_pk(self, speciality):
        try:
            return self.get(pk=speciality)
        except self.model.DoesNotExist:
            return False
        
    def get_speciality(self, speciality):
        try:
            return self.get(speciality=speciality)
        except self.model.DoesNotExist:
            return False
    
    def create_speciality(self, data, employee):
        speciality = self.model()
        speciality.speciality = data["speciality"]
        speciality.employee = employee
        return speciality
    
    def update_speciality(self, speciality, data):
        speciality.speciality = data["speciality"]
        
    def search_speciality(self, speciality):
        try:
            return self.filter(speciality__icontains=speciality)
        except Exception:
            return False
        

class DoctorManager(Manager):
    def get_all_doctors(self):
        return self.all()
    
    def get_doctor_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
        
    def created_doctor(self, data, employee, speciality, status):
        doctor = self.model()
        doctor.name = data["name"]
        doctor.last_name = data["last_name"]
        doctor.type_document = data["type_document"]
        doctor.document = data["document"]
        doctor.phone = data["phone"]
        doctor.speciality = speciality
        doctor.status = status
        doctor.employee = employee
        return doctor
    
    def updated_doctor(self, document, data, speciality, status, employee):
        try:
            doctor = self.get(document=document)
            doctor.name = data["name"]
            doctor.last_name = data["last_name"]
            doctor.type_document = data["type_document"]
            doctor.document = data["document"]
            doctor.phone = data["phone"]
            doctor.speciality = speciality
            doctor.status = status
            doctor.employee = employee
            return doctor
        except self.model.DoesNotExist:
            return False
        
    def get_doctor_by_pk(self, pk):
        try:
            return self.get(pk=pk)
        except self.model.DoesNotExist:
            return False

    def search_doctor(self, search):
        try:
            return self.filter(
               Q(name__icontains=search) | Q(last_name__icontains=search) | Q(document__icontains=search)
            )
        except Exception:
            return False
        
    def get_doctor_by_speciality(self, pk):
        return self.filter(speciality=pk)