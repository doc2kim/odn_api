from rest_framework import serializers
from .models import Measure, Buoy, Location, Sensor1, Sensor2, Sensor3
from drf_spectacular.utils import extend_schema_field, OpenApiTypes
from django_filters import FilterSet, AllValuesFilter, Filter, DateFromToRangeFilter, TimeRangeFilter, NumberFilter
from django_filters.widgets import SuffixedMultiWidget
from django.forms import MultiValueField, FloatField, NumberInput
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

        #     return data.get('slug', None)
        # except AttributeError:
        #     return None

    # @extend_schema_field(MeasureSerializer(many=True))
    # def get_measure(self, obj):
    #     #     # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
    #     page_size = self.context['request'].query_params.get('size') or 10
    # #     # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.
    #     paginator = Paginator(obj.measure.all(), page_size)
    # #     # 사용자가 특정 페이지를 요청할 수 있도록 하려면 query_params를 다시 사용하여 수신.
    #     page = self.context['request'].query_params.get('page') or 1
    #     try:
    #         paginate = paginator.page(page)
    #         serializer = MeasureSerializer(paginate, many=True)

    #     except EmptyPage:
    #         return "no pages"

    #     return serializer.data


class BuoySerializer(serializers.ModelSerializer):
    results = LocationSerializer(source='location', many=True)

    class Meta:
        model = Buoy
        fields = ['buoy_id', 'owner', 'battery', "results"]

    # next = serializers.SerializerMethodField(
    #     'next_paginated')
    # previous = serializers.SerializerMethodField(
    #     'previous_paginated')

        # 페이지 크기를 동적으로 만들기 위해 query_params를 사용하여 원하는 페이지 크기를 수신.
        # page_size = self.context['request'].query_params.get('size') or 10
        # django.core.paginator에 있는 Paginator를 사용하여 반복 가능한 객체에 페이지네이션한다.

    # @extend_schema_field(OpenApiTypes.NUMBER)
    # def data_count(self, obj):
    #     paginator = self.get_paginate(obj)
    #     return paginator.count

    # @extend_schema_field(OpenApiTypes.STR)
    # def next_paginated(self, obj):
    #     paginator = self.get_paginate(obj)
    #     # 사용자가 특정 페이지를 요청할 수 있도록 하려면 query_params를 다시 사용하여 수신.
    #     page = self.context['request'].query_params.get('page') or 1

    #     current_url = self.context['request'].build_absolute_uri()
    #     url = urlparse(current_url)
    #     try:
    #         paginate = paginator.page(page)
    #         # 다음 페이지가 매겨진 데이터에서 대상 페이지를 가져옴.
    #         next_page_num = paginate.next_page_number() if paginate.has_next() else ''

    #         if 'page=' in url.query:
    #             current_number = url.query.split('page=', 1)[1]
    #             next_query = url.query.replace(
    #                 f'page={current_number}', f'page={next_page_num}')
    #             next_page = f'{url.scheme}://{url.netloc}{url.path}?{next_query}' if paginate.has_next(
    #             ) else 'no pages'
    #         else:

    #             next_query = url.query + '&page=%s' % (next_page_num)
    #             next_page = f'{url.scheme}://{url.netloc}{url.path}?{next_query}' if paginate.has_next(
    #             ) else 'no pages'

    #     except EmptyPage:
    #         return "no pages"

    #     return next_page

    # @extend_schema_field(OpenApiTypes.STR)
    # def previous_paginated(self, obj):
    #     paginator = self.get_paginate(obj)
    #     page = self.context['request'].query_params.get('page') or 1
    #     current_url = self.context['request'].build_absolute_uri()
    #     url = urlparse(current_url)
    #     try:
    #         paginate = paginator.page(page)
    #         # 다음 페이지가 매겨진 데이터에서 대상 페이지를 가져옴.
    #         previous_page_num = paginate.previous_page_number() if paginate.has_previous() else ''
    #         if 'page=' in url.query:
    #             current_number = url.query.split('page=', 1)[1]
    #             previous_query = url.query.replace(
    #                 f'page={current_number}', f'page={previous_page_num}')
    #             previous_page = f'{url.scheme}://{url.netloc}{url.path}?{previous_query}' if paginate.has_previous(
    #             ) else 'no pages'

    #         else:

    #             previous_query = url.query + \
    #                 '&page=%s' % (previous_page_num)
    #             previous_page = f'{url.scheme}://{url.netloc}{url.path}?{previous_query}' if paginate.has_previous(
    #             ) else 'no pages'

    #         # 페이지 없음 예외처리
    #     except EmptyPage:
    #         return "no data"

    #     return previous_page


class CustomWidget(SuffixedMultiWidget):
    suffixes = ['lat', 'lon']

    def __init__(self, attrs=None):
        widgets = [
            NumberInput(attrs={'step': '0.0001', 'placeholder': '위도'}),
            NumberInput(attrs={'step': '0.0001', 'placeholder': '경도'}),
        ]
        super().__init__(widgets, attrs)


class CustomField(MultiValueField):
    widget = CustomWidget

    def __init__(self, fields=None, *args, **kwargs):
        if fields is None:
            fields = (
                FloatField(),
                FloatField()
            )
            super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            return list(data_list)
        return [None, None]


class CustomFilter(Filter):
    field_class = CustomField


class DataFilter(FilterSet):
    buoy_id = AllValuesFilter(label="스마트부표 아이디")
    location = CustomFilter(
        method="lat_lon_filter", label="GPS 좌표")
    range_date = DateFromToRangeFilter(
        method="range_date_filter", label="범위 날짜")
    range_time = TimeRangeFilter(
        method="range_time_filter", label="범위 시간")

    class Meta:
        model = Buoy
        fields = ["buoy_id", "location", "range_date", "range_time"]

    def lat_lon_filter(self, queryset, name, value):
        if value[0] and value[1] is not None:
            queryset = queryset.prefetch_related(
                Prefetch('location', queryset=Location.objects.filter(latitude=value[0], longitude=value[1])))
        return queryset

    def range_date_filter(self, queryset, name, value):
        queryset = queryset.prefetch_related(Prefetch(
            'location__measure', queryset=Measure.objects.filter(date__range=[value.start, value.stop]), to_attr='date_range'))
        return queryset

    def range_time_filter(self, queryset, name, value):
        queryset = queryset.prefetch_related(Prefetch(
            'location__measure', queryset=Measure.objects.filter(time__range=[value.start, value.stop])))
        return queryset
