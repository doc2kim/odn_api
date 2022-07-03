from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiParameter,  extend_schema_view
from .serializers import BuoySerializer
from .models import Buoy
from .serializers import DataFilter
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework import status
# from rest_framework.response import Response


@extend_schema_view(
    list=extend_schema(
        summary="스마트부표 측정값 및 상태정보",
        description="""
        • Buoy
            - id : 스마트부표 아이디
            - voltage : 스마트부표 전압

            • Coordinate
                - lat : 위도
                - lon : 경도

                • Measure Time
                    - date : 측정 날짜
                    - time : 측정 시간

                    • Measure
                        - temp: 온도(℃)
                        - oxy: 용존산소 (mg/L)
                        - ph : 산성도(pH)
                        - ppt : 염도(ppt)
                        - orp : 산화환원전위(mV)
                        - c4e : 전기전도도(uS/cm)
        """,
        parameters=[
            OpenApiParameter(
                name='size',
                type=int,
                description="한 페이지당 데이터 출력 개수 </br> ※ Default = 10",
                required=False,
            ),
            OpenApiParameter(
                name='id',
                type=int,
                description="스마트부표 아이디",
                required=False,
            ),
            OpenApiParameter(
                name='lat',
                type=float,
                description="GPS 위도 ",
                required=False,
            ),
            OpenApiParameter(
                name='lon',
                type=float,
                description="GPS 경도",
                required=False,
            ),
            OpenApiParameter(
                name='range_date_after',
                type=str,
                description="범위검색 시작날짜 'yyyy-mm-dd' </br> ※ 단일 날짜 검색시 시작/종료 날짜 동일하게 요청",
                required=False
            ),
            OpenApiParameter(
                name='range_date_before',
                type=str,
                description="범위검색 종료날짜 'yyyy-mm-dd'",
                required=False
            ),
            OpenApiParameter(
                name='range_time_after',
                type=str,
                description="범위검색 시작시간 'hh:mm:ss </br> ※ 단일 시간 검색시 시작/종료 시간 동일하게 요청",
                required=False
            ),
            OpenApiParameter(
                name='range_time_before',
                type=str,
                description="범위검색 종료시간 'hh:mm:ss'",
                required=False
            ),
        ]
    ),
)
class BuoyDataView(ModelViewSet):
    model = Buoy
    serializer_class = BuoySerializer
    queryset = Buoy.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = DataFilter
