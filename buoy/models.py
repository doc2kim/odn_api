from django.db import models
from django_filters import DateFromToRangeFilter, FilterSet,  TimeRangeFilter, AllValuesFilter

# Create your models here.


class Buoy(models.Model):
    id = models.IntegerField(
        help_text="Buoy ID", default=1, primary_key=True)
    voltage = models.FloatField(null=True)

    def __str__(self):
        return '{}'.format(self.id)


class Coordinate(models.Model):
    buoy_id = models.ForeignKey(
        Buoy, related_name="coordinate", on_delete=models.CASCADE, null=True, db_column="buoy_id")
    lat = models.FloatField()
    lon = models.FloatField()

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)


class MeasureTime(models.Model):
    coordinate = models.ForeignKey(
        Coordinate, related_name="measure_time", on_delete=models.CASCADE, null=True, db_column="coordinate_id")
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return '{}, {}'.format(self.date, self.time)


class Measure(models.Model):
    measure_time = models.ForeignKey(
        MeasureTime, related_name="measure", on_delete=models.CASCADE, null=True, db_column="measure_time_id")
    temp = models.FloatField()
    oxy = models.FloatField()
    ph = models.FloatField()
    ppt = models.FloatField()
    orp = models.IntegerField()
    c4e = models.IntegerField()
    crc = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.crc)


class DataFilter(FilterSet):
    id = AllValuesFilter()
    lat = AllValuesFilter(field_name="coordinate__lat")
    lon = AllValuesFilter(field_name="coordinate__lon")
    date = DateFromToRangeFilter(field_name="coordinate__measure_time__date")
    time = TimeRangeFilter(field_name="coordinate__measure_time__time")

    class Meta:
        model = Buoy
        fields = ["id", "lat", "lon", "date", "time"]
