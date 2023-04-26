from django.urls import path

# views
from .views import RegisterCiteView
from .views import DetailCiteView

urlpatterns = [
    path("cites/", RegisterCiteView.as_view(), name="cites"),
    path("cite/<int:pk>/", DetailCiteView.as_view(), name="detail_cite"),
]