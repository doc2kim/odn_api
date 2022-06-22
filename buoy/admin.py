from re import A
from django.contrib import admin
from .models import Buoy, Coordinate, MeasureTime, Measure
# Register your models here.


@admin.register(Buoy)
class BuoyAdmin(admin.ModelAdmin):
    """Buoy Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "id",
                "voltage",

            )
        }),
    )

    list_display = (
        "id",
        "voltage",
    )

    list_filter = (
        "id",
        "voltage",
    )


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    """Measures Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "buoy_id",
                "lat",
                "lon",

            )
        }),
    )

    list_display = (
        "lat",
        "lon"
    )

    list_filter = (
        "lat",
        "lon"
    )


@admin.register(MeasureTime)
class MeasuresTimeAdmin(admin.ModelAdmin):
    """MeasuresTime Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "coordinate",
                "date",
                "time",
            ),
        }),
    )

    list_display = (
        "date",
        "time",
    )

    list_filter = (
        "date",
        "time",
    )


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    """Measure Admin Definition"""

    fieldsets = (
        ("Data", {
            "fields": (
                "measure_time",
                "temp",
                "oxy",
                "ph",
                "ppt",
                "orp",
                "c4e",
            ),
        }),
        ("etc", {
            "fields": (
                "crc",
            ),
        }),
    )

    list_display = (
        "temp",
        "oxy",
        "ph",
        "ppt",
        "orp",
        "c4e",
        "crc",
    )

    list_filter = (
        "temp",
        "oxy",
        "ph",
        "ppt",
        "orp",
        "c4e",
        "crc",
    )
