from rest_framework import serializers
from .models import Measure, Buoy, Location, Sensor1, Sensor2, Sensor3
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django.core.paginator import Paginator, EmptyPage
from urllib.parse import urlparse
from django_filters import FilterSet, AllValuesFilter, DateFromToRangeFilter, TimeRangeFilter
from django.db.models import Prefetch


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

    class Meta:
        model = Location
        fields = ['latitude', 'longitude', 'measure']

    @extend_schema_field(MeasureSerializer(many=True))
    def get_measure(self, obj):
        #     # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
        page_size = self.context['request'].query_params.get('size') or 10
    #     # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.

        paginator = Paginator(obj.measure.all(), page_size)
    #     # 사용자가 특정 페이지를 요청할 수 있도록 하려면 query_params를 다시 사용하여 수신.
        page = self.context['request'].query_params.get('page') or 1
        try:
            paginate = paginator.page(page)
            serializer = MeasureSerializer(paginate, many=True)

        except EmptyPage:
            return "no pages"

        return serializer.data


class BuoySerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True)
    count = serializers.SerializerMethodField(
        'data_count')
    next = serializers.SerializerMethodField(
        'next_paginated')
    previous = serializers.SerializerMethodField(
        'previous_paginated')

    class Meta:
        model = Buoy
        fields = ['count', 'next', 'previous',
                  'buoy_id', 'owner', 'battery', "location", ]

    def get_paginate(self, obj):
        locate = obj.location.all()

        for i in locate:
            # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
            page_size = self.context['request'].query_params.get('size') or 10
            # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.
            paginator = Paginator(i.measure.all(), page_size)
        return paginator

    @extend_schema_field(OpenApiTypes.NUMBER)
    def data_count(self, obj):
        paginator = self.get_paginate(obj)
        return paginator.count

    @extend_schema_field(OpenApiTypes.STR)
    def next_paginated(self, obj):
        paginator = self.get_paginate(obj)
        # 사용자가 특정 페이지를 요청할 수 있도록 하려면 query_params를 다시 사용하여 수신.
        page = self.context['request'].query_params.get('page') or 1
        current_url = self.context['request'].build_absolute_uri()
        url = urlparse(current_url)
        try:
            paginate = paginator.page(page)
            # 다음 페이지가 매겨진 데이터에서 대상 페이지를 가져옴.
            next_page_num = paginate.next_page_number() if paginate.has_next() else ''
            if 'page=' in url.query:
                current_number = url.query.split('page=', 1)[1]
                next_query = url.query.replace(
                    f'page={current_number}', f'page={next_page_num}')
                next_page = f'{url.scheme}://{url.netloc}{url.path}?{next_query}' if paginate.has_next(
                ) else 'no pages'
            else:

                next_query = url.query + '&page=%s' % (next_page_num)
                next_page = f'{url.scheme}://{url.netloc}{url.path}?{next_query}' if paginate.has_next(
                ) else 'no pages'
        except EmptyPage:
            return "데이터 없다"

        return next_page

    @extend_schema_field(OpenApiTypes.STR)
    def previous_paginated(self, obj):
        paginator = self.get_paginate(obj)
        page = self.context['request'].query_params.get('page') or 1
        current_url = self.context['request'].build_absolute_uri()
        url = urlparse(current_url)
        try:
            paginate = paginator.page(page)
            # 다음 페이지가 매겨진 데이터에서 대상 페이지를 가져옴.
            previous_page_num = paginate.previous_page_number() if paginate.has_previous() else ''
            if 'page=' in url.query:
                current_number = url.query.split('page=', 1)[1]
                previous_query = url.query.replace(
                    f'page={current_number}', f'page={previous_page_num}')
                previous_page = f'{url.scheme}://{url.netloc}{url.path}?{previous_query}' if paginate.has_previous(
                ) else 'no pages'

            else:

                previous_query = url.query + \
                    '&page=%s' % (previous_page_num)
                previous_page = f'{url.scheme}://{url.netloc}{url.path}?{previous_query}' if paginate.has_previous(
                ) else 'no pages'

            # 페이지 없음 예외처리
        except EmptyPage:
            return "no data"

        return previous_page


class DataFilter(FilterSet):

    buoy_id = AllValuesFilter(label="스마트부표 아이디")
    latitude = AllValuesFilter(field_name="location__latitude", label="위도")
    longitude = AllValuesFilter(field_name="location__longitude", label="경도")
    range_date = DateFromToRangeFilter(
        method="range_date_filter", label="범위 날짜")
    range_time = TimeRangeFilter(
        method="range_time_filter", label="범위 시간")

    # date = DateFilter(method="single_date_filter", label="단일 날짜")

    class Meta:
        model = Buoy
        fields = ["buoy_id", "latitude", "longitude", "range_date"]

    # def single_date_filter(self, queryset, name, value):
    #     query_id = self.request.query_params.get('id')
    #     query_lat = self.request.query_params.get('lat')
    #     query_lon = self.request.query_params.get('lon')

    #     buoy = self._meta.model.objects.all() if query_id == "" else self._meta.model.objects.filter(id=query_id) if query_lat == "" and query_lon == "" else self._meta.model.objects.filter(
    #         id=query_id, coordinate__lat=query_lat, coordinate__lon=query_lon)

    #     queryset = buoy.prefetch_related(Prefetch(
    #         'coordinate__measure_time', queryset=MeasureTime.objects.filter(date=value)))
    #     return queryset

    def range_date_filter(self, queryset, name, value):
        query_id = self.request.query_params.get('buoy_id')
        query_lat = self.request.query_params.get('latitude')
        query_lon = self.request.query_params.get('longitude')

        buoy = self._meta.model.objects.all() if query_id == "" else self._meta.model.objects.filter(buoy_id=query_id) if query_lat == "" and query_lon == "" else self._meta.model.objects.filter(
            buoy_id=query_id, location__latitude=query_lat, location__longitude=query_lon)

        queryset = buoy.prefetch_related(Prefetch(
            'location__measure', queryset=Measure.objects.filter(date__range=[value.start, value.stop])))
        return queryset

    def range_time_filter(self, queryset, name, value):
        query_id = self.request.query_params.get('buoy_id')
        query_lat = self.request.query_params.get('latitude')
        query_lon = self.request.query_params.get('longitude')
        query_range_date_after = self.request.query_params.get(
            'range_date_after')
        query_range_date_before = self.request.query_params.get(
            'range_date_before')

        buoy = self._meta.model.objects.all() if query_id == "" else self._meta.model.objects.filter(buoy_id=query_id) if query_lat == "" or query_lon == "" else self._meta.model.objects.filter(
            buoy_id=query_id, location__latitude=query_lat, location__longitude=query_lon)

        queryset = buoy.prefetch_related(Prefetch(
            'location__measure', queryset=Measure.objects.filter(time__range=[value.start, value.stop]))) if query_range_date_after == "" or query_range_date_before == "" else buoy.prefetch_related(Prefetch(
                'location__measure', queryset=Measure.objects.filter(date__range=[query_range_date_after, query_range_date_before], time__range=[value.start, value.stop])))

        return queryset
