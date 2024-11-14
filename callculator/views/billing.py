from django.utils.dateparse import parse_date
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from datetime import date
import re

from callculator.models import Call
from callculator.serializers import BillingResponseSerializer

PHONE_NUMBER_REGEX = re.compile(r"^\d{2}\d{8,9}$")


@extend_schema(
    summary="Billings",
    description="Retrieve billing information by phone number and optional date reference.",
    tags=["billing"],
    parameters=[
        OpenApiParameter(
            name="phone_number",
            description="Phone number in the format 'AAXXXXXXXXX'",
            required=True,
            type=str,
        ),
        OpenApiParameter(
            name="dateref",
            description="Date reference in the format 'YYYY-MM'. If not provided, defaults to the last valid month.",
            required=False,
            type=str,
        ),
    ],
    responses={200: BillingResponseSerializer},
    auth=[],
)
class BillingViewSet(viewsets.GenericViewSet):
    @action(methods=["get"], detail=False)
    def billing(self, request, *args, **kwargs):
        phone_number = request.query_params.get("phone_number")
        dateref = request.query_params.get("dateref")

        if not phone_number:
            return Response(
                {"error": "phone_number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not PHONE_NUMBER_REGEX.match(phone_number):
            return Response(
                {"phone_number": "Invalid phone number format"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if dateref:
            dateref = parse_date(dateref + "-01")

            if not dateref:
                return Response(
                    {"dateref": "Invalid date format. Use 'YYYY-MM'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            curr_date = date.today().replace(day=1)
            if dateref >= curr_date:
                return Response(
                    {"dateref": "There is no avaible billing for this dateref."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            today = date.today()
            dateref = (
                date(today.year, today.month - 1, 1)
                if today.month > 1
                else date(today.year - 1, 12, 1)
            )

        response_serializer = BillingResponseSerializer(
            {
                "phone_number": phone_number,
                "dateref": dateref,
            }
        )

        return Response(response_serializer.data, status=status.HTTP_200_OK)
