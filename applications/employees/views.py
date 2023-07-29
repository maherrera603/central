from django.shortcuts import render
#rest
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

# models
from applications.users.models import Role
from applications.users.models import User
from .models import Employee

# serializers
from .serializers import EmployeeResponseSerializer
from .serializers import EmployeeSerializer
from .serializers import EmployeeSearchSerializer
from .serializers import UpdatedEmployeeSerializer

# permissions
from applications.users.permissions import IsAdministrator
from applications.users.permissions import IsEmployee


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
        serializer = EmployeeResponseSerializer(employees, many=True)
        data = _send_data(200, "OK", "Listado de empleados")
        data["employees"] = serializer.data
        return Response(data)

    def post(self, request):
        admin = Employee.objects.get_user(request.user)
        if not admin:
            data = _send_data(404, "not found", "El usuario no se encuentra registrado")
            return Response(data)

        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            data = _send_data(400, "bad request", "Complete los campos requeridos")
            data["errors"] = serializer.errors
            return Response(data)

        user = User.objects.get_user_by_email(serializer.data["user"]["email"])
        if user:
            data = _send_data(400, "bad request", "El usuario ya se encuentra registrado")
            return Response(data)

        role = Role.objects.get_rol(3)
        if not role:
            data = _send_data(404, "not found", "no se encontro el rol")
            return Response(data)
        

        userCreated = User.objects.create_user(serializer.data["user"]["email"], serializer.data["user"]["password"], role)
        employee = Employee.objects.create_employee(serializer.data, userCreated)
        employee.save()

        data = _send_data(202, "created", "Empleado registrado correctamente")
        data["employee"] = serializer.data
        return Response(data)


class DeleteEmployeeView(APIView):
    authentication_classes = (TokenAuthentication, )
    permission_classes = [IsAdministrator]

    def delete(self, request, document):
        employee =  Employee.objects.get_employee_by_document(document)
        user = User.objects.get_user_by_email(email=employee.user.email)
        if not employee or not user:
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
        employee = Employee.objects.get_employee_by_document(document=document)
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
        if not employee:
            data = _send_data(404, "not found", "El empleado no ha sido encontrado")
            return Response(data)

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


class SearchEmployeesView(APIView):
    authentication_classes = (TokenAuthentication ,)
    permission_classes = [IsAdministrator]

    def get(self, request, search):
        admin = Employee.objects.get_user(request.user)
        if not admin:
            data = _send_data(404, "not found", "no se encontro el usuario")
            return Response(data)

        employees = Employee.objects.search_employees(search)
        if len(employees) == 0:
            data = _send_data(404, "not found", "no se encontro ningun resultado")
            return Response(data)

        serializer = EmployeeResponseSerializer(employees, many=True)
        data = _send_data(200, "OK", "list employees")
        data["employees"] = serializer.data
        return Response(data)