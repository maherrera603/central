from django.db.models import Manager


class EmployeeManager(Manager):
    def get_user(self, account):
        return self.get(id_user=account)
    
    def create_employee(self, data, user):
        employee = self.model()
        employee.name = data["name"]
        employee.lastname = data["lastname"]
        employee.type_document = data["type_document"]
        employee.document = data["document"]
        employee.phone = data["phone"]
        employee.id_user = user
        return employee
    
    def employee_exists(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
        
    def get_all_employees(self):
        return self.all().exclude(id_user__id_role_id=1)
    
    def get_employee_by_document(self, document):
        try:
            return self.get(document=document)
        except self.model.DoesNotExist:
            return False
        
    def updated_employee(self, document, data):
        employee = self.get(document=document)
        employee.name = data["name"]
        employee.lastname = data["lastname"]
        employee.phone = data["phone"]
        return employee
    
    def get_employee_by_user(self, user):
        try: 
            return self.get(id_user=user)
        except self.model.DoesNotExist:
            return False
    