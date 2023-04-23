from django.urls import path

# views
from .views import RegisterCiteView

urlpatterns = [
    path('cites/', RegisterCiteView.as_view(), name="cites")
]