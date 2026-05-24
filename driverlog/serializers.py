import re
from datetime import date

from rest_framework import serializers

from driverlog.models import Driverlog
special_characters = set('@_!#$%^&*()<>?/\\|}{~:')


class DriverLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driverlog
        fields = [
            "id",
            "log_date",
            "driver_number",
            "driver_signature",
            "co_driver_name",
            "driver_initials",
            "vehicle_number",
            "trailer_number",
            "total_miles_today",
            "total_mileage_today",
            "operating_center_name_address",
            "total_off_duty_time",
            "total_sleeper_time",
            "total_driving_time",
            "total_on_duty_time",
            "shipper",
            "commodity",
            "load_no",
            "route",
            "created_at",
            "updated_at"
        ]

    def validate_log_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Log date cannot be less than today's date.")
        return value

    # common alphanumeric validator
    def validate_alphanumeric(self, value, field_name):
        if not re.match(r'^[A-Za-z0-9]+$', str(value)):
            raise serializers.ValidationError(f"{field_name} should contain only letters and numbers.")
        return value

    def validate_co_driver_name(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("Co Driver name must be at most 20 characters long.")
        if any(char in special_characters for char in value):
            raise serializers.ValidationError("Co Driver name must contain only letters.")
        return value

    def validate_shipper(self, value):
        if len(value) > 25:
            raise serializers.ValidationError("Shipper number must be less than 25.")
        if any(char in special_characters for char in value):
            raise serializers.ValidationError("Shipper number must contain only letters")
        return value

    def validate_commodity(self, value):
        if len(value) > 25:
            raise serializers.ValidationError("Commodity number must be less than 25.")
        if any(char in special_characters for char in value):
            raise serializers.ValidationError("Commodity number must contain only letters.")
        return value

    def validate_driver_number(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("Driver number must be less than 15.")
        return self.validate_alphanumeric(value, "Driver number")

    def validate_driver_initials(self, value):
        if len(value) > 5:
            raise serializers.ValidationError("Driver initials must be less than 5 characters.")
        return self.validate_alphanumeric(value, "Driver initials")

    def validate_vehicle_number(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("Vehicle number must be less than 15.")
        return self.validate_alphanumeric(value, "Vehicle number")

    def validate_trailer_number(self, value):
        if len(value) > 15:
            raise serializers.ValidationError("Trailer number must be less than 15.")
        return self.validate_alphanumeric(value, "Trailer number")

    def validate_load_no(self, value):
        if len(value) > 20:
            raise serializers.ValidationError("Load number must be less than 20 characters.")
        return self.validate_alphanumeric(value, "Load number")


    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['driver_name'] = f"{instance.route.created_by.first_name} {instance.route.created_by.last_name}"
        data['route_name'] = f"{instance.route.pickup_location} - {instance.route.dropoff_location}"
        return data
