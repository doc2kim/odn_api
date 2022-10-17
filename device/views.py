from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.views.generic.base import TemplateView
from django.core.serializers import serialize

import json

from .models import Device, Location, Oxygen, Ph, Conduct, Chlorophyll
from .serializers import DeviceSerializer, LocationSerializer, OxygenSerializer, PhSerializer, ConductSerializer, ChlorophyllSerializer
from .customs import CustomModelViewSet, CustomFilterBackend


class DevicesView(ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def retrieve(self, request, pk):
        device = get_object_or_404(self.get_queryset(), device_id=pk)
        serializer = self.serializer_class(device)
        return Response(serializer.data)


class LocationView(CustomModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [CustomFilterBackend]


class OxygenView(CustomModelViewSet):
    queryset = Oxygen.objects.all()
    serializer_class = OxygenSerializer
    filter_backends = [CustomFilterBackend]


class PhView(CustomModelViewSet):
    queryset = Ph.objects.all()
    serializer_class = PhSerializer
    filter_backends = [CustomFilterBackend]


class ConductView(CustomModelViewSet):
    queryset = Conduct.objects.all()
    serializer_class = ConductSerializer
    filter_backends = [CustomFilterBackend]


class ChlorophyllView(CustomModelViewSet):
    queryset = Chlorophyll.objects.all()
    serializer_class = ChlorophyllSerializer
    filter_backends = [CustomFilterBackend]


class DeviceMapView(TemplateView):

    template_name = "device/map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)

        """-----2022/10/12 최신 위치 데이터만 보내기 로직 구현----"""
        context["device"] = json.loads(
            serialize("geojson", Location.objects.all()))
        return context


# @api_view(['GET'])
# def devices(request):
#     queryset = Device.objects.all()
#     serializer = DeviceSerializer(queryset, many=True)

#     return Response(serializer.data)


# @api_view(['GET'])
# def device(request, pk):
#     print(pk)
#     queryset = get_object_or_404(Device, device_id=pk)
#     serializer = DeviceSerializer(queryset)
#     return Response(serializer.data)


# from drf_spectacular.utils import extend_schema
# from drf_spectacular.utils import OpenApiParameter,  extend_schema_view


# @extend_schema_view(
#     list=extend_schema(
#         summary="스마트부표 측정값 및 상태정보",
#         description="""
#         • device
#             - id : 스마트부표 아이디
#             - owner : 부표 소유자
#             - battery : 스마트부표 배터리 잔량(%)

#             • location
#                 - latitude : 위도
#                 - longitude : 경도

#                 • measure
#                     - serial_number: 멀티 브로브 제품번호
#                     - date : 측정 날짜
#                     - time : 측정 시간

#                     • sensor1
#                         - serial_number: 센서 제품번호
#                         - temperature : 온도(℃)
#                         - oxygen_per: 용존산소 (%)
#                         - oxygen_mpl: 용존산소 (mg/L)
#                         - oxygen_ppm: 용존산소 (ppm)

#                     • sensor2
#                         - serial_number: 센서 제품번호
#                         - temperature : 온도(℃)
#                         - ph : 수소이온농도(pH)
#                         - redox : 산화환원반응(mV)
#                         - ph_meter : 수소이온농도(mV)

#                     • sensor3
#                         - serial_number: 센서 제품번호
#                         - temperature : 온도(℃)
#                         - conductivity : 전기전도도(μS/cm)
#                         - salinity : 염도(ppt)
#                         - tds : 총 용존 고용물(ppm)

#         """,
#         parameters=[
#             OpenApiParameter(
#                 name='device_id',
#                 type=str,
#                 description='스마트 부표 아이디',
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='location_lat',
#                 type=str,
#                 description='위도',
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='location_lon',
#                 type=str,
#                 description='경도',
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='size',
#                 type=int,
#                 description="한 페이지당 데이터 출력 개수 </br> ※ Default = 10",
#                 required=False,
#             ),
#             OpenApiParameter(
#                 name='scope_date_start',
#                 type=str,
#                 description="범위검색 시작날짜 'yyyy-mm-dd' </br> ※ 단일 날짜 검색시 시작/종료 날짜 동일하게 요청",
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='scope_date_stop',
#                 type=str,
#                 description="범위검색 종료날짜 'yyyy-mm-dd'",
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='scope_time_start',
#                 type=str,
#                 description="범위검색 시작시간 'hh:mm:ss </br> ※ 단일 시간 검색시 시작/종료 시간 동일하게 요청",
#                 required=False
#             ),
#             OpenApiParameter(
#                 name='scope_time_stop',
#                 type=str,
#                 description="범위검색 종료시간 'hh:mm:ss",
#                 required=False
#             ),
#         ]
#     ),
# )
