from django.urls import path
#
from .views import (
    RegisterPattientView, UpdatedPattientView, FamilyView, DetailFamilyView
)


urlpatterns = [
    path('register/', RegisterPattientView.as_view(), name='register_pattient'),
    path('pattient/<str:document>/', UpdatedPattientView.as_view(), name='updated_pattient'),
    path('family/', FamilyView.as_view(), name='add_family'),
    path('family/<int:pk>/', DetailFamilyView.as_view(), name='add_family'),
    
]