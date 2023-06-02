from django.urls import path
# views
from .views import RegisterEmployeeView
from .views import DeleteEmployeeView 
from .views import UpdateProfileEmployee
from .views import SearchEmployeesView

urlpatterns = [
    path("employee-register/", RegisterEmployeeView.as_view(), name="employee-register"),
    path("employee-delete/<str:document>/", DeleteEmployeeView.as_view(), name="employee-delete"),
    path("detail-employee/<str:document>/", UpdateProfileEmployee.as_view(), name="employee-profile"),
    path("employee/search/<str:search>/", SearchEmployeesView.as_view(), name="employee-search"),
]