from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers import DataSerializer
from .models import Data



class BuoyDataView(generics.ListAPIView):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['buoy_id','location','date','time']
