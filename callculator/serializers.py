import re
from datetime import datetime
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils import timezone

from callculator.models import Call, CallRecord


PHONE_NUMBER_REGEX = re.compile(r"^\d{2}\d{8,9}$")


class HealthCheckResponseSerializer(serializers.Serializer):
    """Response Ok."""

    service = serializers.CharField(default="callculator")
    status = serializers.CharField(default="OK")
    database = serializers.CharField()
    time = serializers.CharField(
        default=datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    )


class CallRecordSerializer(serializers.Serializer):
    id = serializers.IntegerField(help_text="Record unique identifier", read_only=True)
    type = serializers.ChoiceField(
        choices=["START", "END"],
        help_text="Indicate if it is a 'START' or 'END' call record",
    )
    timestamp = serializers.CharField(help_text="Timestamp from when the event happens")
    call_id = serializers.IntegerField(help_text="Call")
    source = serializers.CharField(required=False, help_text="Source phone number")
    destination = serializers.CharField(
        required=False, help_text="Destination phone number"
    )

    def validate(self, data):
        if "source" in data and not PHONE_NUMBER_REGEX.match(data["source"]):
            raise serializers.ValidationError(
                {
                    "source": "Invalid phone number. It must be in the format AAXXXXXXXXX."
                }
            )

        if "destination" in data and not PHONE_NUMBER_REGEX.match(data["destination"]):
            raise serializers.ValidationError(
                {
                    "destination": "Invalid phone number. It must be in the format AAXXXXXXXXX."
                }
            )

        if data["type"] == "START" and "source" not in data:
            raise serializers.ValidationError(
                {"source": "Is required for START record"}
            )

        if data["type"] == "START" and "destination" not in data:
            raise serializers.ValidationError(
                {"destination": "Is required for START record"}
            )

        return data

    def create(self, data):
        call, _ = Call.objects.get_or_create(pk=data["call_id"])

        match data["type"]:
            case "START":
                call.source = data["source"]
                call.destination = data["destination"]
                call.start = timezone.make_aware(
                    datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                )

            case "END":
                call.end = timezone.make_aware(
                    datetime.strptime(data["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
                )
            case _:
                raise serializers.ValidationError({"type": "Must be 'START' or 'END'"})

        call.save()

        call_record = CallRecord.objects.create(record_type=data["type"], call=call)

        return {**data, "id": call_record.id}


class CallSerializer(serializers.Serializer):
    destination = serializers.CharField()
    date = serializers.DateField(read_only=True)
    time = serializers.TimeField(read_only=True)
    duration = serializers.DurationField()
    cost = serializers.FloatField()

    class Meta:
        model = Call
        fields = ["destination", "date", "time", "duration", "cost"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.start:
            representation["date"] = instance.start.date()
            representation["time"] = instance.start.time()

        if instance.duration:
            representation["duration"] = self.format_duration(instance.duration)

        if instance.cost:
            representation["cost"] = self.format_cost(instance.cost)

        return {
            "destination": representation["destination"],
            "date": representation["date"],
            "time": representation["time"],
            "duration": representation["duration"],
            "cost": representation["cost"],
        }

    def format_duration(self, duration) -> str:
        if not duration:
            return "0h00m00s"

        total_seconds = int(duration.total_seconds())

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        return f"{hours}h{minutes:02}m{seconds:02}s"

    def format_cost(self, cost: float) -> str:
        return f"R$ {cost:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class BillingResponseSerializer(serializers.Serializer):
    dateref = serializers.DateField(format="%Y-%m", required=False)
    phone_number = serializers.CharField()
    records = CallSerializer(many=True, read_only=True)

    @staticmethod
    def get_filtered_calls(phone_number: str, dateref: None):
        return Call.objects.filter(
            source=phone_number,
            end__date__year=dateref.year,
            end__date__month=dateref.month,
        )

    def to_representation(self, instance):
        phone_number = instance["phone_number"]
        dateref = instance.get("dateref")

        if not dateref:
            today = date.today()
            first_of_month = today.replace(day=1)
            last_month = first_of_month - timedelta(days=1)
            dateref = last_month

        calls = self.get_filtered_calls(phone_number, dateref)

        return {
            "phone_number": phone_number,
            "dateref": dateref,
            "records": CallSerializer(calls, many=True).data,
        }
