from django_filters.rest_framework import DjangoFilterBackend
from .serializers import BuoySerializer
from drf_spectacular.utils import OpenApiExample, OpenApiParameter,  extend_schema_view
from rest_framework.viewsets import ModelViewSet
from drf_spectacular.utils import extend_schema
from .models import Buoy, DataFilter


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
                name='id',
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
                description="범위검색 시작날짜 'yyyy-mm-dd'",
                required=False
            ),
            OpenApiParameter(
                name='date_before',
                type=str,
                description="범위검색 종료날짜 'yyyy-mm-dd'",
                required=False
            ),
            OpenApiParameter(
                name='time_after',
                type=str,
                description="범위검색 시작시간 'hh:mm:ss'",
                required=False
            ),
            OpenApiParameter(
                name='time_before',
                type=str,
                description="범위검색 종료시간 'hh:mm:ss'",
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
    serializer_class = BuoySerializer
    queryset = Buoy.objects.all()
    filter_backends = [DjangoFilterBackend]
    filter_class = DataFilter

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
