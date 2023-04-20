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
            self.get(document=document)
            return True
        except self.model.DoesNotExist:
            return False