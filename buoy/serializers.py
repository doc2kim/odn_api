from rest_framework import serializers
from .models import Data, Buoy, Location


class BuoySerializer(serializers.ModelSerializer):
    class Meta:
        model = Buoy
        fields = ['buoy_id', 'voltage']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['lat', 'lon']


class DataSerializer(serializers.ModelSerializer):
    buoy = BuoySerializer(read_only=True)
    location = LocationSerializer(read_only=True)

    class Meta:
        model = Data
        fields = ['buoy', 'location', 'temp', 'oxy', 'ph',
                  'ppt', 'orp', 'c4e', 'crc', 'date', 'time']
