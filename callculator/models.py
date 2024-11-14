from django.db import models

from callculator.tools import call_cost_calculator


class Call(models.Model):
    source = models.CharField(max_length=11)
    destination = models.CharField(max_length=11)

    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    duration = models.DurationField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start and self.end:
            self.duration = self.end - self.start
            self.cost = call_cost_calculator(self.start, self.end)

        super().save()


class CallRecord(models.Model):
    class Type(models.TextChoices):
        START = "START"
        END = "END"

    record_type = models.CharField(max_length=5, choices=Type.choices)
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
