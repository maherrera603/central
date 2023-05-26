from django.urls import path

# views
from .views import RegisterCiteView
from .views import DetailCiteView
from .views import SearchCiteView

urlpatterns = [
    path("cites/", RegisterCiteView.as_view(), name="cites"),
    path("cite/<int:pk>/", DetailCiteView.as_view(), name="detail_cite"),
    path("cite/search/<str:search>/", SearchCiteView.as_view(), name="search_cite")
]