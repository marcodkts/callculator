from datetime import datetime
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import ViewSet

from callculator.apps import CallculatorConfig
from callculator.serializers import HealthCheckResponseSerializer


@extend_schema(
    summary=_("Health Check endpoint"),
    description=_("Return simple health check."),
    responses={200: HealthCheckResponseSerializer},
    tags=["health"],
    auth=[],
)
class HealthCheckViewSet(ViewSet):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]

    @action(methods=["get"], detail=False)
    def health_check(self, request):
        user_count = User.objects.count()
        app_name = CallculatorConfig.name

        payload = {
            "service": app_name,
            "status": "OK",
            "database": f"OK ({user_count})",
            "time": datetime.utcnow().isoformat(),
        }
        return Response(payload)
