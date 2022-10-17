from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.gis.db import models
from geopy.geocoders import Nominatim


class Device(models.Model):

    DEVICE_MOUNT = 'mounted'
    DEVICE_BUOY = 'buoy'

    DEVICE_CHOICES = {
        (DEVICE_BUOY, 'Buoy'),
        (DEVICE_MOUNT, 'Mounted')
    }
    # device_id = models.IntegerField(help_text="Device ID",  null=True, default='')
    device_id = models.IntegerField(help_text="Device ID",  primary_key=True)
    device_type = models.CharField(
        choices=DEVICE_CHOICES, max_length=50, blank=True, default=DEVICE_BUOY, help_text='디바이스 타입')
    battery = models.FloatField(null=True, help_text="배터리 잔량")
    owner = models.CharField(
        max_length=200, default="ODN", help_text='소유자')

    serial_number = models.CharField(
        max_length=50, help_text="멀티 프로브 제품번호", default="SN-TRIPA-")
    first_run_time = models.DateTimeField(
        auto_now_add=True, help_text='가동시작시간')
    operating_state = models.BooleanField(default=True, help_text='가동상태')

    class Meta:
        ordering = ['device_id']

    def __str__(self):
        return '{}'.format(self.device_id)


class Location(models.Model):
    device = models.ForeignKey(
        Device, related_name="location", on_delete=models.CASCADE, db_column="device_id")
    measured_time = models.DateTimeField(auto_now_add=True, help_text="측정 시간")
    state = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, blank=True, null=True)
    locality = models.CharField(max_length=200, blank=True, null=True)
    coordinate = ArrayField(models.FloatField(), blank=True, null=True)
    point = models.PointField(blank=False, null=False)

    @property
    def full_address(self):
        if self.address is None:
            return '%s %s' % (self.state, self.locality)
        elif self.locality is None:
            return '%s %s' % (self.state, self.address)
        else:
            return '%s %s %s' % (self.state, self.locality, self.address)

    def save(self, *args, **kwargs):
        geo_locator = Nominatim(user_agent='odn')
        location = geo_locator.reverse(
            "%f, %f" % (self.point.y, self.point.x))
        results = location.raw.get('address')
        if 'province' in results and 'city' in results:
            state = "%s %s" % (results['province'], results['city'])
        elif 'province' in results:
            state = results['province']
        elif 'city' in results:
            state = results['city']
        else:
            state = None

        if 'county' in results or 'borough' in results:
            if 'county' in results:
                locality = results['county']
            else:
                locality = results['borough']
        else:
            locality = None

        if 'village' in results and 'town' in results:
            address = "%s, %s" % (results['town'], results['village'])
        elif 'village' in results:
            address = results['village']
        elif 'town' in results:
            address = results['town']
        else:
            address = None

        self.state = state
        self.locality = locality
        self.address = address
        self.coordinate = self.point.y, self.point.x
        super(Location, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-measured_time']

    def __str__(self):
        return '%s, %s' % (self.full_address, self.coordinate)


class Oxygen(models.Model):
    device = models.ForeignKey(
        Device, related_name="oxygen_sensor", on_delete=models.CASCADE, db_column="device_id")
    measured_time = models.DateTimeField(auto_now_add=True, help_text="측정 시간")
    serial_number = models.CharField(
        max_length=50, help_text="센서 제품번호", default="SN-PODOC-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    oxygen_per = models.FloatField(null=True, help_text="% 용존산소")
    oxygen_mpl = models.FloatField(null=True, help_text="mg/L 용존산소")
    oxygen_ppm = models.FloatField(null=True, help_text="ppm 용존산소")

    class Meta:
        ordering = ['-measured_time']

    def __str__(self):
        return '용존산소 센서 {}'.format(self.measured_time, self.device.device_id, self.serial_number)


class Ph(models.Model):
    device = models.ForeignKey(
        Device, related_name="ph_sensor", on_delete=models.CASCADE, db_column="device_id")
    measured_time = models.DateTimeField(auto_now_add=True, help_text="측정 시간")
    serial_number = models.CharField(
        max_length=50, help_text="센서 제품번호", default="SN-PPHRB-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    ph = models.FloatField(null=True, help_text="pH 수소이온농도")
    redox = models.FloatField(null=True, help_text="mV 산화환원반응")
    ph_meter = models.FloatField(null=True, help_text="mV 수소이온농도_미터")

    class Meta:
        ordering = ['-measured_time']

    def __str__(self):
        return 'pH 센서 {}'.format(self.measured_time, self.device.device_id, self.serial_number)


class Conduct(models.Model):
    device = models.ForeignKey(
        Device, related_name="conduct_sensor", on_delete=models.CASCADE, db_column="device_id")
    measured_time = models.DateTimeField(auto_now_add=True, help_text="측정 시간")
    serial_number = models.CharField(
        max_length=50, help_text="센서 제품번호", default="SN-PC4EB-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    conductivity = models.FloatField(null=True, help_text="μS/cm 전도도")
    salinity = models.FloatField(null=True, help_text="ppt 염도")
    tds = models.FloatField(null=True, help_text="ppm 용존 고용물")

    class Meta:
        ordering = ['-measured_time']

    def __str__(self):
        return '전도도 센서 {}'.format(self.measured_time, self.device.device_id, self.serial_number)


class Chlorophyll(models.Model):
    device = models.ForeignKey(
        Device, related_name="chlorophyll_sensor", on_delete=models.CASCADE, db_column="device_id")
    measured_time = models.DateTimeField(auto_now_add=True, help_text="측정 시간")
    serial_number = models.CharField(
        max_length=50, help_text="센서 제품번호", default="SN-")
    temperature = models.FloatField(null=True, help_text="℃ 수온")
    chlorophyll = models.FloatField(null=True, help_text="ug/L")

    class Meta:
        ordering = ['-measured_time']

    def __str__(self):
        return '엽록소 센서 {}'.format(self.measured_time, self.device.device_id, self.serial_number)
