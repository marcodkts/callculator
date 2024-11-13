from datetime import datetime, timedelta
from django.conf import settings


def call_cost_calculator(start: datetime, end: datetime):
    counter = start
    minutes = 0
    while counter < end:
        if int(settings.RATE_START) <= counter.hour < int(settings.RATE_END):
            minutes += 1
        counter += timedelta(minutes=1)

    payable_time = (minutes * 60 - counter.second + end.second) // 60
    return float(settings.INITIAL_COST) + (payable_time * float(settings.MINUTE_COST))
