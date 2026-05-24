from django.contrib.gis.db.models import PointField
from django.db import models

from tms_auth.models import AuthUser, BaseModel


class Route(BaseModel):
    current_location = PointField(srid=4326, null=True, blank=True)
    pickup_location = PointField(srid=4326, null=True, blank=True)
    dropoff_location = PointField(srid=4326, null=True, blank=True)
    created_by = models.ForeignKey(AuthUser, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        app_label = 'route'
        db_table = 'route'
