from django.urls import path

# views
from .views import RegisterCiteView
from .views import DetailCiteView
from .views import SearchCiteView
from .views import AllCitesView
from .views import SearchCiteForEmployee
from .views import DetailCiteForEmployeeView

urlpatterns = [
    path("cites/", RegisterCiteView.as_view(), name="cites"),
    path("cite/<int:pk>/", DetailCiteView.as_view(), name="detail_cite"),
    path("cite/search/<str:search>/", SearchCiteView.as_view(), name="search_cite"),
    path("allCites/", AllCitesView.as_view(), name="all_cites"),
    path("cites/search/<str:search>/", SearchCiteForEmployee.as_view(), name="search_cite_for_employee"),
    path("citeForEmployee/<int:pk>/", DetailCiteForEmployeeView.as_view(), name="detail_cite_for_employee"),
]