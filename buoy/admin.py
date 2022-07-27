
from django.contrib import admin
from .models import Buoy, Location, Measure, Sensor1, Sensor2, Sensor3
# Register your models here.


@admin.register(Buoy)
class BuoyAdmin(admin.ModelAdmin):
    """Buoy Admin Definition"""
    fieldsets = (
        ("Info", {
            "fields": (
                "buoy_id",
                "battery",
                "owner"
            )
        }),
    )

    list_display = (
        "buoy_id",
        "battery",
        "owner"
    )

    list_filter = (
        "buoy_id",
        "battery",
        "owner"
    )


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Measures Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "buoy",
                "latitude",
                "longitude",

            )
        }),
    )

    list_display = (
        "latitude",
        "longitude"
    )

    list_filter = (
        "latitude",
        "longitude"
    )


@admin.register(Sensor1)
class Sensor1Admin(admin.ModelAdmin):
    """Sensor1 Admin Definition"""
    fieldsets = (
        ("SensorInfo", {
            "fields": (
                "serial_number",
            )
        }
        ),
        ("Value", {
            "fields": (
                "temperature",
                "oxygen_per",
                "oxygen_mpl",
                "oxygen_ppm",
            ),
        }
        )
    )


@admin.register(Sensor2)
class Sensor2Admin(admin.ModelAdmin):
    """Sensor2 Admin Definition"""
    fieldsets = (
        ("SensorInfo", {
            "fields": (
                "serial_number",
            )
        }
        ),
        ("Value", {
            "fields": (
                "temperature",
                "ph",
                "redox",
                "ph_meter",
            ),
        }
        )
    )


@admin.register(Sensor3)
class Sensor3Admin(admin.ModelAdmin):
    """Sensor3 Admin Definition"""
    fieldsets = (
        ("Info", {
            "fields": (
                "serial_number",
            )
        }
        ),
        ("Value", {
            "fields": (
                "temperature",
                "conductivity",
                "salinity",
                "tds",
            ),
        }
        )
    )


@admin.register(Measure)
class MeasureAdmin(admin.ModelAdmin):
    """Measure Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "location",
                "serial_number",
            ),
        }),
        ("Datetime", {
            "fields": (
                "date",
                "time",
            ),
        }),
        ("SensorData", {
            "fields": (
                "sensor1",
                "sensor2",
                "sensor3",
            ),
        }),
        ("etc", {
            "fields": (
                "crc",
            ),
        }),
    )

    list_display = (
        "serial_number",
        "date",
        "time",
        "crc",
    )

    list_filter = (
        "serial_number",
        "date",
        "time",
        "crc",
    )
