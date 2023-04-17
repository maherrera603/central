from django.db.models import Manager


class EmployeeManager(Manager):
    def get_user(self, account):
        return self.get(id_user=account)