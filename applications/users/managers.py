from django.db.models import Manager
from django.contrib.auth.models import BaseUserManager

class RoleManager(Manager):
    pass


class UserManager(BaseUserManager, Manager):
    def _created_user(self, email, password, rol, is_staff, is_superuser):
        user = self.model()
        user.email = email
        user.id_rol = rol
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, email, password):
        return self._created_user(email, password, 1, True, True)
    
    def create_user(self, email, password, rol):
        return self._created_user(email, password, rol, False, False)