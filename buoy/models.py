from django.db import models


class Buoy(models.Model):
    buoy_id = models.IntegerField(
        help_text="Buoy ID",  primary_key=True)
    battery = models.FloatField(null=True, help_text="배터리 잔량")
    owner = models.CharField(
        max_length=200, default="ODN", help_text='스마트부표 소유자')

    def __str__(self):
        return '{}'.format(self.buoy_id)


class Location(models.Model):
    buoy = models.ForeignKey(
        Buoy, related_name="location", on_delete=models.PROTECT, db_column="buoy_id")
    latitude = models.FloatField(help_text="위도")
    longitude = models.FloatField(help_text="경도")

    def __str__(self):
        return '{}, {}'.format(self.latitude, self.longitude)


class Sensor1(models.Model):
    serial_number = models.CharField(
        max_length=50, help_text="제품번호", default="SN-PODOC-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    oxygen_per = models.FloatField(null=True, help_text="% 용존산소")
    oxygen_mpl = models.FloatField(null=True, help_text="mg/L 용존산소")
    oxygen_ppm = models.FloatField(null=True, help_text="ppm 용존산소")

    def __str__(self):
        return '센서1 {}'.format(self.serial_number)


class Sensor2(models.Model):
    serial_number = models.CharField(
        max_length=50, help_text="제품번호", default="SN-PPHRB-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    ph = models.FloatField(null=True, help_text="pH 수소이온농도")
    redox = models.FloatField(null=True, help_text="mV 산화환원반응")
    ph_meter = models.FloatField(null=True, help_text="mV 수소이온농도_미터")

    def __str__(self):
        return '센서2 {}'.format(self.serial_number)


class Sensor3(models.Model):
    serial_number = models.CharField(
        max_length=50, help_text="제품번호", default="SN-PC4EB-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    conductivity = models.FloatField(null=True, help_text="μS/cm 전도도")
    salinity = models.FloatField(null=True, help_text="ppt 염도")
    tds = models.FloatField(null=True, help_text="ppm 용존 고용물")

    def __str__(self):
        return '센서3 {}'.format(self.serial_number)


class Measure(models.Model):
    location = models.ForeignKey(
        Location, related_name="measure", on_delete=models.CASCADE, db_column="location_id")
    serial_number = models.CharField(
        help_text="멀티 프로브 제품번호", max_length=50, default="SN-TRIPA-")
    date = models.DateField(help_text="측정 일자")
    time = models.TimeField(help_text="측정 시간")
    sensor1 = models.OneToOneField(
        Sensor1, related_name="sensor1", on_delete=models.CASCADE, null=True, db_column="sensor1_id")
    sensor2 = models.OneToOneField(
        Sensor2, related_name="sensor2", on_delete=models.CASCADE, null=True, db_column="sensor2_id")
    sensor3 = models.OneToOneField(
        Sensor3, related_name="sensor3", on_delete=models.CASCADE, null=True, db_column="sensor3_id")
    crc = models.CharField(null=True, max_length=50, help_text="crc16-modbus")

    class Meta:
        ordering = ['-date', '-time']

    def __str__(self):
        return '{} - {} / {}'.format(self.location, self.date, self.time)
