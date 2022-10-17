
from django.contrib import admin
from django.contrib.gis.admin import OSMGeoAdmin
from .models import Device, Location, Oxygen, Ph, Conduct, Chlorophyll


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    """Device Admin Definition"""
    readonly_fields = ['first_run_time']
    fieldsets = (
        ("Info", {
            "fields": (
                "device_id",
                "device_type",
                "battery",
                "owner",
                "first_run_time",
                "operating_state",
            )
        }),
    )
    list_display = (
        "owner",
        "device_id",
        "device_type",
        "battery",
        "first_run_time",
        "operating_state",
    )
    list_filter = (
        "device_id",
        "owner",
        "device_type",
        "battery",
        "first_run_time",
        "operating_state",
    )


@admin.register(Location)
class LocationAdmin(OSMGeoAdmin):
    """Location Admin Definition"""
    default_lon = 129
    default_lat = 35.184
    default_zoom = 10
    readonly_fields = ('measured_time', 'coordinate', 'full_address')
    fieldsets = (
        ("Info", {
            "fields": (
                "device",
                "measured_time",
                "state",
                "locality",
                "address",
                "full_address",
                "coordinate",
                "point",
            )
        }),
    )

    list_display = (
        "coordinate",
        "state",
        "locality",
        "address",
        "measured_time",
        "device"
    )

    list_filter = (
        "measured_time",
        "state",
        "locality",
        "address",
        "device"
    )


@admin.register(Oxygen)
class OxygenAdmin(admin.ModelAdmin):
    """Oxygen Admin Definition"""
    readonly_fields = ['measured_time']
    fieldsets = (
        ("SensorInfo", {
            "fields": (
                "device",
                "serial_number",
                "measured_time",
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
    list_display = (
        "serial_number",
        "measured_time",
        "device",
    )

    list_filter = (
        "serial_number",
        "measured_time",
        "device",
    )


@admin.register(Ph)
class PhAdmin(admin.ModelAdmin):
    readonly_fields = ['measured_time']
    """Ph Admin Definition"""
    fieldsets = (
        ("SensorInfo", {
            "fields": (
                "device",
                "serial_number",
                "measured_time",
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
    list_display = (
        "serial_number",
        "measured_time",
        "device",
    )

    list_filter = (
        "serial_number",
        "measured_time",
        "device",
    )


@admin.register(Conduct)
class ConductAdmin(admin.ModelAdmin):
    """Conduct Admin Definition"""
    readonly_fields = ['measured_time']
    fieldsets = (
        ("SensorInfo", {
            "fields": (
                "device",
                "serial_number",
                "measured_time",
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
    list_display = (
        "serial_number",
        "measured_time",
        "device",
    )

    list_filter = (
        "serial_number",
        "measured_time",
        "device",
    )


@admin.register(Chlorophyll)
class ChlorophyllAdmin(admin.ModelAdmin):
    """Chlorophyll Admin Definition"""
    readonly_fields = ['measured_time']
    fieldsets = (
        ("Info", {
            "fields": (
                "device",
                "serial_number",
                "measured_time",
            )
        }
        ),
        ("Value", {
            "fields": (
                "temperature",
                "chlorophyll",
            ),
        }
        )
    )
    list_display = (
        "serial_number",
        "measured_time",
        "device",
    )

    list_filter = (
        "serial_number",
        "measured_time",
        "device",
    )
