
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ml_models.planner import generate_plans

from .models import ConfirmedTrip
from .serializers import ConfirmedTripSerializer, PlanRequestSerializer

logger = logging.getLogger("travel_planner.trips")

# Currency exchange rates to MAD
EXCHANGE_RATES = {
    "MAD": 1,
    "USD": 10.2,
    "EUR": 11.1,
    "GBP": 12.5,
    "JPY": 0.072,
}

class PlanView(APIView):
    def post(self, request):
        serializer = PlanRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            logger.debug("Validated plan request: %s", data)

            currency = data['currency']
            exchange_rate = EXCHANGE_RATES.get(currency, 1)
            mad_budget = data['budget'] * exchange_rate

            result = generate_plans(
                budget=mad_budget,
                region=data['region'],
                lifestyle=data['lifestyle']
            )

            logger.info("Generated plans for region=%s, lifestyle=%s, currency=%s", data['region'], data['lifestyle'], currency)
            return Response(result, status=status.HTTP_200_OK)

        logger.warning("Plan request validation failed: %s", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmTripView(APIView):
    def post(self, request):
        try:
            selected_plan = request.data.get('selectedPlan')
            region = request.data.get('region')
            budget = request.data.get('budget')
            currency = request.data.get('currency')
            lifestyle = request.data.get('lifestyle')

            if not selected_plan or not selected_plan.get('id'):
                logger.warning("Confirm trip attempted without selectedPlan id")
                return Response({"error": "selectedPlan with id is required"}, status=400)

            trip = ConfirmedTrip.objects.create(
                region=region,
                budget=budget,
                currency=currency,
                lifestyle=lifestyle,
                selected_plan=selected_plan
            )

            serializer = ConfirmedTripSerializer(trip)
            return Response({
                "status": "confirmed",
                "message": "Trip successfully saved!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("Failed to confirm trip: %s", e, exc_info=True)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ConfirmedTripsListView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        lifestyle = request.query_params.get('lifestyle')

        trips = ConfirmedTrip.objects.all()

        if region:
            trips = trips.filter(region__iexact=region)
        if lifestyle:
            trips = trips.filter(lifestyle__iexact=lifestyle)

        trips = trips.order_by('-created_at')
        logger.info("Listing confirmed trips filters region=%s lifestyle=%s count=%s", region, lifestyle, trips.count())
        serializer = ConfirmedTripSerializer(trips, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
