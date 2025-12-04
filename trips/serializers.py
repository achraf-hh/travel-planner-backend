"""Serializers for validating trip planning and confirmation payloads."""

from rest_framework import serializers

from .models import ConfirmedTrip


class PlanRequestSerializer(serializers.Serializer):
    """Validate incoming plan generation requests."""

    budget = serializers.FloatField()
    currency = serializers.CharField()
    region = serializers.CharField()
    lifestyle = serializers.CharField()


class ConfirmTripSerializer(serializers.Serializer):
    """Validate the payload when persisting a selected plan."""

    region = serializers.CharField()
    budget = serializers.FloatField()
    currency = serializers.CharField()
    lifestyle = serializers.CharField()
    selectedPlan = serializers.JSONField()


class ConfirmTripByIdSerializer(serializers.Serializer):
    """Validate confirmation payloads that refer to a plan by id."""

    plan_id = serializers.CharField()
    region = serializers.CharField()
    currency = serializers.CharField()
    budget = serializers.FloatField()
    lifestyle = serializers.CharField()


class ConfirmedTripSerializer(serializers.ModelSerializer):
    """Serialize stored trips back to clients."""

    class Meta:
        model = ConfirmedTrip
        fields = "__all__"
