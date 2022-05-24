from django.urls import path
from . import views

urlpatterns = [
    path('', views.BuoyDataView.as_view(), name="buoy"),
]