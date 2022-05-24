from rest_framework import generics
from .serializers import DataSerializer
from .models import Data


class BuoyDataView(generics.ListAPIView):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
