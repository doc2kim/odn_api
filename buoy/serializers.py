from rest_framework import serializers
from .models import Measure, Buoy, Coordinate, MeasureTime


class MeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measure
        fields = ['temp', 'oxy', 'ph', 'ppt', 'orp', 'c4e']


class MeasureTimeSerializer(serializers.ModelSerializer):
    measure = MeasureSerializer(many=True, read_only=True)

    class Meta:
        model = MeasureTime
        fields = ['date', 'time', 'measure']


class CoordinateSerializer(serializers.ModelSerializer):
    measure_time = MeasureTimeSerializer(many=True, read_only=True)

    class Meta:
        model = Coordinate
        fields = ['lat', 'lon', "measure_time"]


class BuoySerializer(serializers.ModelSerializer):
    coordinate = CoordinateSerializer(many=True)

    class Meta:
        model = Buoy
        fields = ['id', 'voltage', "coordinate"]
