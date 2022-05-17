from django.contrib import admin
from .models import Buoy, Location, Data
# Register your models here.


@admin.register(Buoy)
class BuoyAdmin(admin.ModelAdmin):
    """Opendata Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "buoy_id",
                "voltage"
            )
        }),
    )

    list_display = (
        "buoy_id",
        "voltage"
    )

    list_filter = (
        "buoy_id",
        "voltage"
    )
    
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    """Opendata Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "buoy",
                "lat",
                "lon"
            )
        }),
    )

    list_display = (
        "buoy",
        "lat",
        "lon"
    )

    list_filter = (
        "buoy",
        "lat",
        "lon"
    )
    
@admin.register(Data)
class DataAdmin(admin.ModelAdmin):
    """Opendata Admin Definition"""

    fieldsets = (
        ("Info", {
            "fields": (
                "buoy",
                "location",
            ),
        }),
        ("Time", {
            "fields": (
                "date",
                "time"
            ),
        }),
        ("Data", {
            "fields": (
                "temp",
                "oxy",
                "ph",
                "ppt",
                "orp",
                "o4e",
            ),
        }),
        ("etc", {
            "fields": (
                "crc",
            ),
        }),
    )

    list_display = (
        "buoy",
        "location",
        "date",
        "time",
        "temp",
        "oxy",
        "ph",
        "ppt",
        "orp",
        "o4e"
    )
    


    list_filter = (
        "buoy",
        "location",
        "date",
        "time",
        "temp",
        "oxy",
        "ph",
        "ppt",
        "orp",
        "o4e"
    )