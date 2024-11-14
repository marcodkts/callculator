from rest_framework.routers import DefaultRouter

from callculator.apps import CallculatorConfig
from callculator.views.billing import BillingViewSet
from callculator.views.callrecord import CallRecordViewSet
from callculator.views.health import HealthCheckViewSet

base_path = CallculatorConfig.name
router = DefaultRouter()

router.register(base_path, CallRecordViewSet, basename="callrecord")
router.register(base_path, BillingViewSet, basename="billing")
router.register(base_path, HealthCheckViewSet, basename="health_check")
