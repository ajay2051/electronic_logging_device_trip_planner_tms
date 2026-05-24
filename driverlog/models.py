from django.db import models

from route.models import Route
from tms_auth.models import AuthUser, BaseModel


class Driverlog(BaseModel):
    log_date = models.DateField()
    driver_number = models.CharField(max_length=10, null=True, blank=True)
    driver_signature = models.CharField(max_length=100, null=True, blank=True)
    co_driver_name = models.CharField(max_length=50, null=True, blank=True)
    driver_initials = models.CharField(max_length=10, null=True, blank=True)
    vehicle_number = models.CharField(max_length=50, null=True, blank=True)
    trailer_number = models.CharField(max_length=50, null=True, blank=True)
    total_miles_today = models.CharField(null=True, blank=True)
    total_mileage_today = models.CharField(null=True, blank=True)
    operating_center_name_address = models.CharField(max_length=50, null=True, blank=True)
    total_off_duty_time = models.CharField(null=True, blank=True)
    total_sleeper_time = models.CharField(null=True, blank=True)
    total_driving_time = models.CharField(null=True, blank=True)
    total_on_duty_time = models.CharField(null=True, blank=True)
    shipper = models.CharField(max_length=50, null=True, blank=True)
    commodity = models.CharField(max_length=50, null=True, blank=True)
    load_no = models.CharField(max_length=50, null=True, blank=True)

    route = models.ForeignKey(Route, on_delete=models.CASCADE)

    class Meta:
        db_table = 'driverlog'
