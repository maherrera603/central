from django.urls import path
# views
from .views import RegisterEmployeeView, DeleteEmployeeView, UpdateProfileEmployee

urlpatterns = [
    path("employee-register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employee-delete/<str:document>/", DeleteEmployeeView.as_view(), name="employee-delete"),
    path("detail-employee/<str:document>/", UpdateProfileEmployee.as_view(), name="employee-profile")
]