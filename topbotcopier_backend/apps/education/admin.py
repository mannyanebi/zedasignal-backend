from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.AcademyVideo)
class AcademyVideoAdmin(admin.ModelAdmin):
    list_display = ("title",)
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]


@admin.register(models.Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "date",
        "time",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]
