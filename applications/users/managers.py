from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager


class RoleManager(Manager):
    def get_role(self, role):
        try:
            return self.get(role__icontains=role)
        except self.model.DoesNotExist:
            return False
    
    def get_rol(self, role):
        return self.get(pk=role)
    
    def get_all_roles(self):
        return self.all().exclude(role="Paciente")
    
    def exists_role(self, role):
        try:
            role = self.get(role=role)
            return False if role.role == "Paciente" else role
        except self.model.DoesNotExist:
            return False
        


class UserManager(BaseUserManager, Manager):
    def _created_user(self, email, password, rol, is_staff, is_superuser):
        user = self.model()
        user.email = email
        user.id_role = rol
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self.db)
        return user

    
    def create_superuser(self, email, password):
        return self._created_user(email, password, None, True, True)
    
    def create_user(self, email, password, rol):
        return self._created_user(email, password, rol, False, False)
           
    def get_user_by_email(self, email):
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return False