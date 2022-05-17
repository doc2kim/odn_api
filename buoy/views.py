from rest_framework import generics
from .serializers import DataSerializer
from .models import Data


class BuoyDataView(generics.ListCreateAPIView):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
