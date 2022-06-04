from django.db import models
from django_filters import DateFromToRangeFilter, FilterSet,  TimeRangeFilter, AllValuesFilter

# Create your models here.


class Buoy(models.Model):
    buoy_id = models.IntegerField(primary_key=True)
    voltage = models.FloatField(null=True)

    def __str__(self):
        return '{}'.format(self.buoy_id)


class Location(models.Model):
    buoy = models.ForeignKey(
        Buoy, related_name='location_buoy', on_delete=models.PROTECT)
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)


class Data(models.Model):
    buoy = models.ForeignKey(
        Buoy, related_name='data_buoy', on_delete=models.PROTECT)
    location = models.ForeignKey(
        Location, related_name='data_location', on_delete=models.PROTECT)
    temp = models.FloatField()
    oxy = models.FloatField()
    ph = models.FloatField()
    ppt = models.FloatField()
    orp = models.IntegerField()
    c4e = models.IntegerField()
    crc = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()

    class Meta:
        ordering = ('-date', '-time')

    def __str__(self):
        return '{}'.format(self.location)


class DataFilter(FilterSet):
    buoy = AllValuesFilter(field_name="buoy__buoy_id")
    lat = AllValuesFilter(field_name="location__lat")
    lon = AllValuesFilter(field_name="location__lon")
    date = DateFromToRangeFilter()
    time = TimeRangeFilter()

    class Meta:
        model = Data
        fields = ["buoy", "lat", "lon", "date", "time"]
