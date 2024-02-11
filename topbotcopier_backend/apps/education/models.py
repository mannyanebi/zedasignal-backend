import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _
from zedasignal_backend.core.mixins import CreatedAndUpdatedAtMixin


# Create your models here.
class AcademyVideo(CreatedAndUpdatedAtMixin, models.Model):
    """
    Academy video model for Zedasignal Backend.
    Stores information and links for academy videos.
    """

    uuid = models.UUIDField(
        _("uuid"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("The unique identifier of this video."),
    )
    title = models.CharField(
        _("title"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The title of this video."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of this video."),
    )
    video_link = models.CharField(
        _("video link"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The video link of this video."),
    )
    thumbnail = models.ImageField(
        _("thumbnail"),
        upload_to="thumbnails/",
        blank=True,
        null=True,
        help_text=_("The thumbnail of this video."),
    )

    def __str__(self):
        return self.title


class Webinar(CreatedAndUpdatedAtMixin, models.Model):
    """
    Webinar model for Zedasignal Backend.
    Stores information and links for webinars.
    """

    uuid = models.UUIDField(
        _("uuid"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("The unique identifier of this video."),
    )
    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of this webinar."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of this webinar."),
    )
    image = models.ImageField(
        _("image"),
        upload_to="webinar/",
        blank=True,
        null=True,
        help_text=_("The image of this webinar."),
    )
    date = models.DateField(
        _("date"),
        blank=True,
        null=True,
        help_text=_("The date of this webinar."),
    )
    time = models.TimeField(
        _("time"),
        blank=True,
        null=True,
        help_text=_("The time of this webinar."),
    )
    location = models.CharField(
        _("location"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The location of this webinar."),
    )

    def __str__(self):
        return self.name
