from django.db.models import Manager
from django.db.models import Q

class EmployeeManager(Manager):
    def get_user(self, account):
        try: 
            return self.get(user=account)
        except self.model.DoesNotExist:
            return False
        
    def create_employee(self, data, user):
        employee = self.model()
        employee.name = data["name"]
        employee.last_name = data["last_name"]
        employee.type_document = data["type_document"]
        employee.document = data["document"]
        employee.phone = data["phone"]
        employee.user = user
        return employee
    
    def get_employee_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
        
    def get_all_employees(self):
        return self.all().exclude(user__role_id=2)
    
        
    def updated_employee(self, document, data):
        try:
            employee = self.get(document=document)
            employee.name = data["name"]
            employee.last_name = data["last_name"]
            employee.phone = data["phone"]
            return employee
        except self.model.DoesNotExist:
            return False
        
    def search_employees(self, search):
        return self.filter(
            Q(name__icontains=search) | Q(last_name__icontains=search) | Q(document__icontains=search)
        ).exclude(user__role_id=2)
        
    
    
    