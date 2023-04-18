from django.urls import  path
# views
from .views import RegisterRoleView, LoginView, LogoutView

urlpatterns = [
    path('roles/', RegisterRoleView.as_view(), name='roles'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]