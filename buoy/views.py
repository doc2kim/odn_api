from django_filters.rest_framework import DjangoFilterBackend
from .serializers import DataSerializer
from drf_spectacular.utils import OpenApiExample, OpenApiParameter,  extend_schema_view
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from .models import Data, DataFilter


@extend_schema_view(
    list=extend_schema(
        summary="스마트부표 측정값 및 상태정보",
        description="""
        • buoy
            - buoy_id : 스마트부표 아이디
            - voltage : 스마트부표 전압

        • location
            - lat : 위도
            - lon : 경도

        • data
            - temp: 온도(℃)
            - oxy: 용존산소 (mg/L)
            - ph : 산성도(pH)
            - ppt : 염도(ppt)
            - orp : 산화환원전위(mV)
            - c4e : 전기전도도(uS/cm)
            - crc : CRC16-MODBUS
            - date : 측정 날짜
            - time : 측정 시간
        """,
        parameters=[
            OpenApiParameter(
                name='buoy',
                type=int,
                description="스마트부표 아이디",
                required=False,
            ),
            OpenApiParameter(
                name='lat',
                type=float,
                description="GPS 위도",
                required=False,
            ),
            OpenApiParameter(
                name='lon',
                type=float,
                description="GPS 경도",
                required=False,
            ),
            OpenApiParameter(
                name='date_after',
                type=str,
                description="범위검색 시작날짜 'yyyy-mm-dd' 입력",
                required=False
            ),
            OpenApiParameter(
                name='date_before',
                type=str,
                description="범위검색 종료날짜 'yyyy-mm-dd' 입력",
                required=False
            ),
            OpenApiParameter(
                name='time_after',
                type=str,
                description="범위검색 시작시간 'hh:mm:ss' 입력",
                required=False
            ),
            OpenApiParameter(
                name='time_before',
                type=str,
                description="범위검색 종료시간 'hh:mm:ss' 입력",
                required=False
            ),
            OpenApiParameter(
                name='page',
                type=int,
                description="페이지 번호",
                required=False
            ),
        ]
    ),
)
class BuoyDataView(ModelViewSet):
    serializer_class = DataSerializer
    queryset = Data.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = DataFilter

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
