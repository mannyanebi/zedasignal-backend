import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class CreatedAtMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

    # https://docs.djangoproject.com/en/3.2/ref/models/options/#abstract
    class Meta:
        abstract = True


class UpdatedAtMixin(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    # https://docs.djangoproject.com/en/3.2/ref/models/options/#abstract
    class Meta:
        abstract = True


class CreatedAndUpdatedAtMixin(CreatedAtMixin, UpdatedAtMixin):
    # https://docs.djangoproject.com/en/3.2/ref/models/options/#abstract
    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
        help_text=_("Unique identifier for this object."),
    )

    # https://docs.djangoproject.com/en/3.2/ref/models/options/#abstract
    class Meta:
        abstract = True
