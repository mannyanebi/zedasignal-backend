from rest_framework import serializers

from zedasignal_backend.apps.education.models import AcademyVideo, Webinar


class AcademyVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademyVideo
        exclude = ("created_at", "updated_at", "id")


class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        exclude = ("created_at", "updated_at", "id")
