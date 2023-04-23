from django.urls import path

# views
from .views import RegisterPattientView 
from .views import UpdatedPattientView 
from .views import FamilyView 
from .views import DetailFamilyView


urlpatterns = [
    path('register/', RegisterPattientView.as_view(), name='register_pattient'),
    path('pattient/<str:document>/', UpdatedPattientView.as_view(), name='updated_pattient'),
    path('family/', FamilyView.as_view(), name='add_family'),
    path('family/<str:document>/', DetailFamilyView.as_view(), name='add_family'),
    
]