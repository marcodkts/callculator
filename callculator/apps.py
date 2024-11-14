from django.apps import AppConfig


class CallculatorConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "callculator"

    def ready(self):
        from callculator.urls import router
        from core.urls import urlpatterns as base_urls

        base_urls.extend(router.urls)

        super().ready()
