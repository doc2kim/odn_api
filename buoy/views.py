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
        • buoy
            - id : 스마트부표 아이디
            - owner : 부표 소유자
            - battery : 스마트부표 배터리 잔량(%)

            • location
                - latitude : 위도
                - longitude : 경도
                
                • measure
                    - serial_number: 멀티 브로브 제품번호
                    - date : 측정 날짜
                    - time : 측정 시간
                    
                    • sensor1
                        - serial_number: 센서 제품번호
                        - temperature : 온도(℃)
                        - oxygen_per: 용존산소 (%)
                        - oxygen_mpl: 용존산소 (mg/L)
                        - oxygen_ppm: 용존산소 (ppm)
                        
                    • sensor2
                        - serial_number: 센서 제품번호
                        - temperature : 온도(℃)
                        - ph : 수소이온농도(pH)
                        - redox : 산화환원반응(mV)
                        - ph_meter : 수소이온농도(mV)
                        
                    • sensor3
                        - serial_number: 센서 제품번호
                        - temperature : 온도(℃)
                        - conductivity : 전기전도도(μS/cm)
                        - salinity : 염도(ppt)
                        - tds : 총 용존 고용물(ppm)
                
        """,
        parameters=[
            OpenApiParameter(
                name='size',
                type=int,
                description="한 페이지당 데이터 출력 개수 </br> ※ Default = 10",
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
