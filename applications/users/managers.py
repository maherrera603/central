from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager


class RoleManager(Manager):
    def rol_exists(self, role):
        try:
            self.get(role=role)
            return True
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
    
    def user_exists(self, email):
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return False
        
    def get_user_by_email(self, email):
        try:
            self.get(email=email)
        except self.model.DoesNotExist:
            return False