from django.urls import  path
# views
from .views import CreateSuperUser, RegisterRoleView, LoginView, LogoutView

urlpatterns = [
    path("admin/", CreateSuperUser.as_view(), name="register-superuser"),
    path("roles/", RegisterRoleView.as_view(), name="roles"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]