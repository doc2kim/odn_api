from rest_framework import serializers
# from rest_framework_gis import serializers
from .customs import CustomSerializer
from .models import Device, Location, Oxygen, Ph, Conduct, Chlorophyll
# from drf_spectacular.utils import extend_schema_field, OpenApiTypes


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ['device_id', 'device_type', 'owner', 'serial_number', 'battery',
                  'first_run_time', 'operating_state']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['measured_time', 'coordinate', 'full_address']


class OxygenSerializer(CustomSerializer):

    class Meta:
        model = Oxygen
        fields = ['serial_number', 'location', 'measured_time', 'temperature',
                  'oxygen_per', 'oxygen_mpl', 'oxygen_ppm']


class PhSerializer(CustomSerializer):

    class Meta:
        model = Ph
        fields = ['serial_number', 'location', 'measured_time',
                  'temperature', 'ph', 'redox', 'ph_meter']


class ConductSerializer(CustomSerializer):

    class Meta:
        model = Conduct
        fields = ['serial_number', 'location', 'measured_time', 'temperature',
                  'conductivity', 'salinity', 'tds']


class ChlorophyllSerializer(CustomSerializer):

    class Meta:
        model = Chlorophyll
        fields = ['serial_number', 'location', 'measured_time',
                  'temperature', 'chlorophyll']
