from rest_framework import filters
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from .models import Location
import datetime


class CustomSerializer(serializers.ModelSerializer):
    location = serializers.SerializerMethodField('get_location')

    def get_location(self, obj):
        date_time = obj.measured_time
        try:
            loc = Location.objects.get(
                device__device_id=obj.device_id,
                measured_time__gt=date_time - timedelta(minutes=1),
                measured_time__lt=date_time + timedelta(minutes=1)
            )
            results = {
                "address": loc.full_address,
                "coordinate": loc.coordinate
            }
        except Location.DoesNotExist:
            results = "doesn't exist"
        return results


class CustomModelViewSet(ModelViewSet):

    def retrieve(self, request, pk):
        filtered_queryset = self.filter_queryset(self.get_queryset())
        # 클래스에서 정의한 filter_backends로 필터링
        queryset = filtered_queryset.filter(device__device_id=pk)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)


class CustomFilterBackend(filters.BaseFilterBackend):

    """datetime filter"""

    def filter_queryset(self, request, queryset, view):
        # request.GET.get or request.query_params.get
        date_time_query = request.query_params.get('date_time', None)
        end_date_time_query = request.query_params.get('end_date_time', None)

        if date_time_query and end_date_time_query:
            if 'T' in date_time_query and end_date_time_query:
                date_time = datetime.datetime.strptime(
                    date_time_query, '%Y-%m-%dT%H:%M:%S')
                end_date_time = datetime.datetime.strptime(
                    end_date_time_query, '%Y-%m-%dT%H:%M:%S')

                queryset = queryset.filter(
                    measured_time__gte=date_time, measured_time__lte=end_date_time)
            else:
                date_time = datetime.datetime.strptime(
                    date_time_query, '%Y-%m-%d')
                end_date_time = datetime.datetime.strptime(
                    end_date_time_query, '%Y-%m-%d')

                queryset = queryset.filter(
                    measured_time__gte=date_time, measured_time__lte=end_date_time + datetime.timedelta(days=1))

        elif date_time_query:
            if 'T' in date_time_query:
                if '.' in date_time_query:
                    date_time = datetime.datetime.strptime(
                        date_time_query, '%Y-%m-%dT%H:%M:%S.%f')
                    queryset = queryset.filter(measured_time__gte=date_time)
                else:
                    date_time = datetime.datetime.strptime(
                        date_time_query, '%Y-%m-%dT%H:%M:%S')
                    queryset = queryset.filter(measured_time__gte=date_time,
                                               measured_time__lte=date_time + datetime.timedelta(minutes=1))
            else:
                date_time = datetime.datetime.strptime(
                    date_time_query, '%Y-%m-%d')

                queryset = queryset.filter(
                    measured_time__gte=date_time, measured_time__lte=date_time + datetime.timedelta(days=1))
        else:
            queryset

        return queryset
