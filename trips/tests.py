from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import ConfirmedTrip


class TripsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_plan_view_returns_plans_for_valid_request(self):
        payload = {
            "region": "Marrakesh",
            "budget": 1000,
            "currency": "USD",
            "lifestyle": "explorer",
        }

        response = self.client.post(reverse("generate-plan"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("plans", response.data)
        self.assertGreater(len(response.data["plans"]), 0)

    def test_plan_view_returns_empty_plans_for_unknown_region(self):
        payload = {
            "region": "Unknownland",
            "budget": 500,
            "currency": "USD",
            "lifestyle": "explorer",
        }

        response = self.client.post(reverse("generate-plan"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"plans": []})

    def test_confirm_trip_creates_record(self):
        payload = {
            "region": "Agadir",
            "budget": 750,
            "currency": "EUR",
            "lifestyle": "explorer",
            "selectedPlan": {
                "id": "1234",
                "title": "Sample Plan",
                "activities": [],
                "accommodation": {"name": "Test Riad"},
            },
        }

        response = self.client.post(reverse("confirm-trip"), payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ConfirmedTrip.objects.count(), 1)
        trip = ConfirmedTrip.objects.first()
        self.assertEqual(trip.region, payload["region"])
        self.assertEqual(trip.lifestyle, payload["lifestyle"])

    def test_confirmed_trips_list_filters(self):
        ConfirmedTrip.objects.create(
            region="Marrakesh",
            budget=1200,
            currency="USD",
            lifestyle="explorer",
            selected_plan={"id": "a"},
        )
        ConfirmedTrip.objects.create(
            region="Agadir",
            budget=900,
            currency="USD",
            lifestyle="comfort_seeker",
            selected_plan={"id": "b"},
        )

        response = self.client.get(
            reverse("confirmed-trips"),
            {"region": "Marrakesh", "lifestyle": "explorer"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["region"], "Marrakesh")
        self.assertEqual(response.data[0]["lifestyle"], "explorer")
