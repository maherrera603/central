from django.urls import path
# views
from .views import RegisterEmployeeView

urlpatterns = [
    path("employee-register/", RegisterEmployeeView.as_view(), name="employee-register")
]