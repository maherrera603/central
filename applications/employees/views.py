from django.shortcuts import render
#rest 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# models
from applications.employees.models import Employee
# serializers

def _send_data(code: int, status: str, message: str):
    data = {}
    data["code"] = code
    data["status"] = status
    data["message"] = message
    return data

# Create your views here.
class RegisterEmployeeView(APIView):
    def post(self, request):
        data = _send_data(200, "OK", "register employee")
        return Response(data)