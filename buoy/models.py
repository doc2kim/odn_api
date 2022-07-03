from django.db import models


# Create your models here.


class Buoy(models.Model):
    id = models.IntegerField(
        help_text="Buoy ID",  primary_key=True)
    voltage = models.FloatField(null=True, help_text="전압")

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return '{}'.format(self.id)


class Coordinate(models.Model):
    buoy_id = models.ForeignKey(
        Buoy, related_name="coordinate", on_delete=models.PROTECT, null=True, db_column="buoy_id")
    lat = models.FloatField(help_text="위도")
    lon = models.FloatField(help_text="경도")

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)


class MeasureTime(models.Model):
    coordinate = models.ForeignKey(
        Coordinate, related_name="measure_time", on_delete=models.PROTECT, null=True, db_column="coordinate_id")
    date = models.DateField(help_text="측정 일자")
    time = models.TimeField(help_text="측정 시간")

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return '{}, {}'.format(self.date, self.time)


class Measure(models.Model):
    measure_time = models.ForeignKey(
        MeasureTime, related_name="measure", on_delete=models.PROTECT, null=True, db_column="measure_time_id")
    temp = models.FloatField(help_text="℃ (수온)")
    oxy = models.FloatField(help_text="mg/L (용존산소)")
    ph = models.FloatField(help_text="pH (산성도)")
    ppt = models.FloatField(help_text="ppt (염도)")
    orp = models.IntegerField(help_text="mV (산화환원전위)")
    c4e = models.IntegerField(help_text="uS/cm (전기전도도)")
    crc = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.crc)
