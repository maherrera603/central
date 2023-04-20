from django.shortcuts import render
#rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# models
from .models import Employee
from applications.users.models import User, Role
# serializers
from .serializers import EmployeeSerializer


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data["code"] = code
    data["status"] = status
    data["message"] = message
    return data


class RegisterEmployeeView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid()

        user = User.objects.user_exists(serializer.data["email"])
        if user is True:
            data = _send_data(400, "bad request", "El usuario ya ha sido registrado")
            return Response(data)
        
        employee_exists = Employee.objects.employee_exists(serializer.data["document"])
        if employee_exists:
            data = _send_data(400, "bad request", "el empleado ya ha sido registrado anteriormente")
            return Response(data)
        
        role = Role.objects.get_rol(serializer.data["role"])
        user = User.objects.create_user(email=serializer.data["email"], password=serializer.data["password"], rol=role)
        employee = Employee.objects.create_employee(serializer.data, user)
        employee.save()
        
        data = _send_data(200, "OK", "empleado ha sido registrado correctamente")
        data["employee"] = serializer.data
        return Response(data)