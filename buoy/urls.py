from django.urls import path
from . import views

urlpatterns = [
    path('buoy/', views.BuoyDataView.as_view(), name="buoy"),
]