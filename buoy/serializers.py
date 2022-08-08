from rest_framework import serializers
from .models import Measure, Buoy, Location, Sensor1, Sensor2, Sensor3
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django_filters import FilterSet, AllValuesFilter
from django.db.models import Prefetch
from .custom_filter import CustomLocationFilter, CustomDateTimeFilter


class Sensor1Serializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor1
        fields = ['serial_number', 'temperature',
                  'oxygen_per', 'oxygen_mpl', 'oxygen_ppm']


class Sensor2Serializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor2
        fields = ['serial_number', 'temperature', 'ph', 'redox', 'ph_meter']


class Sensor3Serializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor3
        fields = ['serial_number', 'temperature',
                  'conductivity', 'salinity', 'tds']


class MeasureSerializer(serializers.ModelSerializer):
    sensor1 = Sensor1Serializer()
    sensor2 = Sensor2Serializer()
    sensor3 = Sensor3Serializer()

    class Meta:
        model = Measure
        fields = ['serial_number', 'date', 'time',
                  'sensor1', 'sensor2', 'sensor3']


class LocationSerializer(serializers.ModelSerializer):
    measure = serializers.SerializerMethodField('get_measure')
    data_count = serializers.SerializerMethodField('get_count')

    class Meta:
        model = Location
        fields = ['data_count', 'latitude', 'longitude', 'measure']

    @extend_schema_field(MeasureSerializer(many=True))
    def get_measure(self, obj):
        size = self.context['request'].query_params.get('size') or 10
        measure = obj.measure.all()

        serializer = MeasureSerializer(measure[:int(size)], many=True) if len(
            measure) >= int(size) else MeasureSerializer(measure, many=True)
        return serializer.data

    @extend_schema_field(OpenApiTypes.INT)
    def get_count(self, obj):
        measure = self.get_measure(obj)

        return len(measure)


class BuoySerializer(serializers.ModelSerializer):
    results = LocationSerializer(source='location', many=True)

    class Meta:
        model = Buoy
        fields = ['buoy_id', 'owner', 'battery', "results"]


class DataFilter(FilterSet):
    buoy_id = AllValuesFilter(label="스마트부표 아이디")
    location = CustomLocationFilter(
        method="lat_lon_filter", label="GPS 좌표")
    scope = CustomDateTimeFilter(
        method="range_date_time_filter", label="일별/시간별 범위 검색")

    class Meta:
        model = Buoy
        fields = ["buoy_id", "location", "scope"]

    def lat_lon_filter(self, queryset, name, value):
        if value[0] and value[1] is not None:
            queryset = queryset.prefetch_related(
                Prefetch('location', queryset=Location.objects.filter(latitude=value[0], longitude=value[1]).select_related('buoy')))
        return queryset

    def range_date_time_filter(self, queryset, name, value):

        if value[0] and value[1] is not None and not value[2] and not value[3]:
            queryset = queryset.prefetch_related(Prefetch(
                'location__measure', queryset=Measure.objects.filter(date__range=[value[0], value[1]]).select_related('location')))

        elif value[2] and value[3] is not None and not value[0] and not value[1]:
            queryset = queryset.prefetch_related(Prefetch(
                'location__measure', queryset=Measure.objects.filter(time__range=[value[2], value[3]]).select_related('location')))

        elif value[0] and value[1] and value[2] and value[3] is not None:
            queryset = queryset.prefetch_related(Prefetch(
                'location__measure', queryset=Measure.objects.filter(date__range=[value[0], value[1]], time__range=[value[2], value[3]]).select_related('location')))

        return queryset
