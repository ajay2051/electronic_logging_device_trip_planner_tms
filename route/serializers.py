import json

from django.contrib.gis.geos import GEOSGeometry
from rest_framework import serializers

from route.models import Route


class RouteSerializer(serializers.ModelSerializer):
    current_location = serializers.JSONField(required=True)
    pickup_location = serializers.JSONField(required=True)
    dropoff_location = serializers.JSONField(required=True)

    class Meta:
        model = Route
        fields = ['id', 'current_location', 'pickup_location', 'dropoff_location', 'created_at', 'updated_at']

    def validate_current_location(self, value):
        return GEOSGeometry(json.dumps(value))

    def validate_pickup_location(self, value):
        return GEOSGeometry(json.dumps(value))

    def validate_dropoff_location(self, value):
        return GEOSGeometry(json.dumps(value))

    def create(self, validated_data):
        return Route.objects.create(**validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['created_by'] = f"{instance.created_by.first_name} {instance.created_by.last_name}"
        for field in ['current_location', 'pickup_location', 'dropoff_location']:
            value = getattr(instance, field, None)
            data[field] = json.loads(value.geojson) if value else None
        return data
