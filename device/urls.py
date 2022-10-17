from django.urls import path
from . import views

urlpatterns = [
    path('', views.DevicesView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/', views.DevicesView.as_view(
        {'get': 'retrieve'}),),

    path('locations/', views.LocationView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/locations/', views.LocationView.as_view(
        {'get': 'retrieve'}),),

    path('oxygens/', views.OxygenView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/oxygens/', views.OxygenView.as_view(
        {'get': 'retrieve'}),),

    path('phs/', views.PhView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/phs/', views.PhView.as_view(
        {'get': 'retrieve'}),),

    path('conducts/', views.ConductView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/conducts/', views.ConductView.as_view(
        {'get': 'retrieve'}),),

    path('chlorophylls/', views.ChlorophyllView.as_view(
        {'get': 'list'}),),
    path('<int:pk>/chlorophylls/', views.ChlorophyllView.as_view(
        {'get': 'retrieve'}),),

    path("map/", views.DeviceMapView.as_view()),
]
