from django.urls import path
from rest_framework.routers import DefaultRouter

from callculator.views.callrecord import CallRecordViewSet
from callculator.views.billing import BillingViewSet
from callculator.views.health import HealthCheckViewSet
from callculator.apps import CallculatorConfig

base_path = CallculatorConfig.name
router = DefaultRouter()

router.register(base_path, CallRecordViewSet, basename="callrecord")
router.register(base_path, BillingViewSet, basename="billing")
router.register(base_path, HealthCheckViewSet, basename="health_check")
