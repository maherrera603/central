from django.shortcuts import render
#rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
# models
from .models import Employee
from applications.users.models import User, Role
# serializers
from .serializers import EmployeeSerializer, UpdatedEmployeeSerializer
# permissions
from applications.users.permissions import IsAdministrator, IsEmployee


# Create your views here.
def _send_data(code: int, status: str, message: str):
    data = {}
    data["code"] = code
    data["status"] = status
    data["message"] = message
    return data


class RegisterEmployeeView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]
    
    def get(self, request):
        employees = Employee.objects.get_all_employees()
        data = _send_data(200, "OK", "Listado de empleados")
        data["employees"] = employees.values()
        return Response(data)
    
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


class DeleteEmployeeView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator] # TODO: add or change permissions adminstrador
    
    def delete(self, request, document):
        isExists = Employee.objects.employee_exists(document=document)
        employee =  Employee.objects.get_employee_by_document(document)
        isExists_user = User.objects.user_exists(email=employee.id_user.email)
        user = User.objects.get_user_by_email(email=employee.id_user.email)
        validate_employee = (not isExists) or (not employee) or (not isExists_user) or (user is False)
       
        if not validate_employee:
            data = _send_data(404, "not found", "El empleado no se encuentra registrado")
            return Response(data)
        
        user.delete()
        employee.delete()
        data = _send_data(204, "not content", "El empleado ha sido eliminado")
        return Response (data)
    

class UpdateProfileEmployee(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsEmployee]
    
    def get(self, request, document):
        employee = Employee.objects.employee_exists(document=document)
        if not employee:
            data = _send_data(404, "bad request", "El empleado no fue encontrado")
            return Response(data)
        
        data = _send_data(200, "OK", "informacion del empleado")
        data["employee"] = {
            "name": employee.name,
            "lasname": employee.lastname,
            "type_document": employee.type_document,
            "document": employee.document,
            "phone": employee.phone,
        }
        return Response(data)
    
    def put(self, request, document):
        serializer = UpdatedEmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Complete los campos de formulario")
            data["errors"]= serializer.errors
            return Response(data)
        
        employee = Employee.objects.updated_employee(document, serializer.data)
        employee.save()
        data = _send_data(202, "created", "datos del empleado actualizados")
        data["employee"] = {
            "id": employee.id,
            "name": employee.name,
            "lastname": employee.lastname,
            "type_document": employee.type_document,
            "document": employee.document,
            "phone": employee.phone,
        }
        return Response(data)
    

