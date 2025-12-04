"""Models for persisted travel plans."""

from django.db import models


class ConfirmedTrip(models.Model):
    """Persisted travel plan selection with request context and chosen plan payload."""

    region = models.CharField(max_length=100)
    budget = models.FloatField()
    currency = models.CharField(max_length=10)
    lifestyle = models.CharField(max_length=100)
    selected_plan = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.region} - {self.lifestyle} ({self.created_at.date()})"
