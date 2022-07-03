from rest_framework import serializers
from .models import Measure, Buoy, Coordinate, MeasureTime
from drf_spectacular.utils import OpenApiTypes, extend_schema_field
from django.core.paginator import Paginator, EmptyPage
from urllib.parse import urlparse
# from drf_spectacular.utils import extend_schema_field
from django_filters import FilterSet, AllValuesFilter, DateFromToRangeFilter, TimeRangeFilter, CharFilter
from django.db.models import Prefetch


class MeasureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Measure
        fields = ['temp', 'oxy', 'ph', 'ppt', 'orp', 'c4e']


class MeasureTimeSerializer(serializers.ModelSerializer):
    measure = MeasureSerializer(many=True)

    class Meta:
        model = MeasureTime
        fields = ['date', 'time', 'measure']


class CoordinateSerializer(serializers.ModelSerializer):
    measure_time = serializers.SerializerMethodField('get_measure_time')

    class Meta:
        model = Coordinate
        fields = ['lat', 'lon', 'measure_time']

    @extend_schema_field(
        {
            'type': "string", 'format': 'binary',
            'example': [
                {
                    "date": "0000-00-00",
                    "time": "00:00:00",
                    "measure": [
                        {
                            "temp": 0,
                            "oxy": 0,
                            "ph": 0,
                            "ppt": 0,
                            "orp": 0,
                            "c4e": 0
                        }
                    ]
                }
            ]
        }
    )
    def get_measure_time(self, obj):
        #     # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
        page_size = self.context['request'].query_params.get('size') or 10
    #     # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.
        paginator = Paginator(obj.measure_time.all(), page_size)
    #     # 사용자가 특정 페이지를 요청할 수 있도록 하려면 query_params를 다시 사용하여 수신.
        page = self.context['request'].query_params.get('page') or 1
        try:
            paginate = paginator.page(page)
            serializer = MeasureTimeSerializer(paginate, many=True)
        except EmptyPage:
            return "데이터 없다"
        return serializer.data


class BuoySerializer(serializers.ModelSerializer):
    coordinate = CoordinateSerializer(many=True)
    count = serializers.SerializerMethodField(
        'data_count')
    next = serializers.SerializerMethodField(
        'next_paginated')
    previous = serializers.SerializerMethodField(
        'previous_paginated')

    class Meta:
        model = Buoy
        fields = ['count', 'next', 'previous',
                  'id', 'voltage', "coordinate"]

    def get_paginate(self, obj):
        coord = obj.coordinate.all()
        for i in coord:
            # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
            page_size = self.context['request'].query_params.get('size') or 10
            # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.
            paginator = Paginator(i.measure_time.all(), page_size)
        return paginator

    def data_count(self, obj):
        paginator = self.get_paginate(obj)
        return paginator.count

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
                ) else '페이지 없다'
            else:

                next_query = url.query + '&page=%s' % (next_page_num)
                next_page = f'{url.scheme}://{url.netloc}{url.path}?{next_query}' if paginate.has_next(
                ) else '페이지 없다'
        except EmptyPage:
            return "데이터 없다"

        return next_page

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
                ) else '페이지 없다'

            else:

                previous_query = url.query + \
                    '&page=%s' % (previous_page_num)
                previous_page = f'{url.scheme}://{url.netloc}{url.path}?{previous_query}' if paginate.has_previous(
                ) else '페이지 없다'

            # 페이지 없음 예외처리
        except EmptyPage:
            return "데이터 없다"

        return previous_page


class DataFilter(FilterSet):
    # print(self.request.query_params.get('size'))
    id = AllValuesFilter(label="스마트부표 아이디")
    lat = AllValuesFilter(field_name="coordinate__lat", label="위도")
    lon = AllValuesFilter(field_name="coordinate__lon", label="경도")
    range_date = DateFromToRangeFilter(
        method="range_date_filter", label="범위 날짜")
    range_time = TimeRangeFilter(
        method="range_time_filter", label="범위 시간")

    # date = DateFilter(method="single_date_filter", label="단일 날짜")

    class Meta:
        model = Buoy
        fields = ["id", "lat", "lon", "range_date"]

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
        query_id = self.request.query_params.get('id')
        query_lat = self.request.query_params.get('lat')
        query_lon = self.request.query_params.get('lon')

        buoy = self._meta.model.objects.all() if query_id == "" else self._meta.model.objects.filter(id=query_id) if query_lat == "" and query_lon == "" else self._meta.model.objects.filter(
            id=query_id, coordinate__lat=query_lat, coordinate__lon=query_lon)

        queryset = buoy.prefetch_related(Prefetch(
            'coordinate__measure_time', queryset=MeasureTime.objects.filter(date__range=[value.start, value.stop])))
        return queryset

    def range_time_filter(self, queryset, name, value):
        query_id = self.request.query_params.get('id')
        query_lat = self.request.query_params.get('lat')
        query_lon = self.request.query_params.get('lon')
        query_range_date_after = self.request.query_params.get(
            'range_date_after')
        query_range_date_before = self.request.query_params.get(
            'range_date_before')

        buoy = self._meta.model.objects.all() if query_id == "" else self._meta.model.objects.filter(id=query_id) if query_lat == "" or query_lon == "" else self._meta.model.objects.filter(
            id=query_id, coordinate__lat=query_lat, coordinate__lon=query_lon)

        queryset = buoy.prefetch_related(Prefetch(
            'coordinate__measure_time', queryset=MeasureTime.objects.filter(time__range=[value.start, value.stop]))) if query_range_date_after == "" or query_range_date_before == "" else buoy.prefetch_related(Prefetch(
                'coordinate__measure_time', queryset=MeasureTime.objects.filter(date__range=[query_range_date_after, query_range_date_before], time__range=[value.start, value.stop])))

        return queryset
