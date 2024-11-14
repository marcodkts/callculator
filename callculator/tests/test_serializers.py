from datetime import datetime, timedelta

from rest_framework.test import APITestCase

from callculator.models import Call, CallRecord
from callculator.serializers import (
    BillingResponseSerializer,
    CallRecordSerializer,
    CallSerializer,
    HealthCheckResponseSerializer,
)

FIXED_TIMESTAMP_START = datetime(2024, 1, 1, 12, 0, 0)
FIXED_TIMESTAMP_END = datetime(2024, 1, 1, 13, 0, 0)


class TestHealthCheckResponseSerializer(APITestCase):
    def test_default_values(self):
        serializer = HealthCheckResponseSerializer(data={"database": "OK"})
        serializer.is_valid()
        data = serializer.data

        self.assertEqual(data["service"], "callculator")
        self.assertEqual(data["status"], "OK")
        self.assertIn("database", data)
        self.assertIn("time", data)
        self.assertRegex(data["time"], r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class TestCallRecordSerializer(APITestCase):
    def setUp(self):
        self.valid_start_data = {
            "type": "START",
            "timestamp": FIXED_TIMESTAMP_START.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "call_id": 1,
            "source": "11987654321",
            "destination": "21998765432",
        }

        self.valid_end_data = {
            "type": "END",
            "timestamp": FIXED_TIMESTAMP_END.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "call_id": 1,
        }

    def test_valid_start_record(self):
        serializer = CallRecordSerializer(data=self.valid_start_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertEqual(Call.objects.count(), 1)
        self.assertEqual(CallRecord.objects.count(), 1)

    def test_valid_end_record(self):
        # Create a START call first
        Call.objects.create(
            pk=1,
            source="11987654321",
            destination="21998765432",
            start=FIXED_TIMESTAMP_START,
        )
        serializer = CallRecordSerializer(data=self.valid_end_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.assertEqual(CallRecord.objects.count(), 1)

    def test_invalid_phone_number(self):
        invalid_data = self.valid_start_data.copy()
        invalid_data["source"] = "1234"  # Invalid phone number
        serializer = CallRecordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("source", serializer.errors)

    def test_missing_source_for_start(self):
        invalid_data = self.valid_start_data.copy()
        del invalid_data["source"]
        serializer = CallRecordSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("source", serializer.errors)


class TestCallSerializer(APITestCase):
    def test_representation_format(self):
        call = Call(
            pk=1,
            source="11987654321",
            destination="21998765432",
            start=FIXED_TIMESTAMP_START,
            end=FIXED_TIMESTAMP_END,
            duration=timedelta(minutes=60),
            cost=12.34,
        )
        serializer = CallSerializer(call)
        data = serializer.data
        self.assertEqual(data["destination"], "21998765432")
        self.assertEqual(data["duration"], "1h00m00s")
        self.assertEqual(data["cost"], "R$ 12,34")


class TestBillingResponseSerializer(APITestCase):
    def setUp(self):
        self.call = Call.objects.create(
            pk=1,
            source="11987654321",
            destination="21998765432",
            start=FIXED_TIMESTAMP_START,
            end=FIXED_TIMESTAMP_END,
            duration=timedelta(minutes=60),
            cost=12.34,
        )

    def test_representation(self):
        instance = {
            "phone_number": "11987654321",
            "dateref": FIXED_TIMESTAMP_START.date(),
        }
        serializer = BillingResponseSerializer()
        data = serializer.to_representation(instance)
        self.assertEqual(data["phone_number"], "11987654321")
        self.assertEqual(len(data["records"]), 1)
        self.assertEqual(data["records"][0]["cost"], "R$ 5,76")
