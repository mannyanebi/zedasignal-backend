from django.contrib import admin

from zedasignal_backend.apps.trading import models


# Register your models here.
@admin.register(models.Signal)
class SignalAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "entry",
        "take_profit",
        "stop_loss",
        "term",
        "action",
        "created_at",
    )
    readonly_fields = ("uuid", "created_at")
