from django.db.models import Manager


class StatusManager(Manager):
    def get_status(self, status):
        try:
            return self.get(status__icontains=status)
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
    
    def get_speciality(self, speciality):
        try:
            return self.get(speciality__icontains=speciality)
        except self.model.DoesNotExist:
            return False
    
    def create_speciality(self, data, employee):
        speciality = self.model()
        speciality.speciality = data["speciality"]
        speciality.id_employee = employee
        return speciality
    
    def update_speciality(self, speciality, data):
        speciality.speciality = data["speciality"]
        


class DoctorManager(Manager):
    pass