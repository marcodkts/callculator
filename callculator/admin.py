from django.contrib import admin

from callculator.models import Call, CallRecord

# Register your models here.
admin.site.register(Call)
admin.site.register(CallRecord)
