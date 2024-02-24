from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import ArrayField

from zedasignal_backend.apps.users.utils import get_custom_user_model
from zedasignal_backend.core.mixins import CreatedAndUpdatedAtMixin, UUIDMixin

User = get_custom_user_model()


# Create your models here.
class Signal(CreatedAndUpdatedAtMixin, UUIDMixin, models.Model):
    """
    Signal model for Zedasignal Backend.
    """

    TERM_LONG = "long"
    TERM_SHORT = "short"
    ACTION_BUY = "buy"
    ACTION_SELL = "sell"

    class SignalTerm(models.TextChoices):
        LONG = "long", "Long"
        SHORT = "short", "Short"

    class SignalAction(models.TextChoices):
        BUY = "buy", "Buy"
        SELL = "sell", "Sell"

    entry = models.FloatField(
        _("entry"),
        blank=False,
        null=False,
        help_text=_("The entry price of the signal."),
    )
    take_profit = models.FloatField(
        _("take profit"),
        blank=False,
        null=False,
        help_text=_("The take profit price of the signal."),
    )
    stop_loss = models.FloatField(
        _("stop loss"),
        blank=False,
        null=False,
        help_text=_("The stop loss price of the signal."),
    )
    term = models.CharField(
        _("term"),
        max_length=5,
        choices=SignalTerm.choices,
        default=SignalTerm.LONG,
        help_text=_("The term of the signal."),
    )
    action = models.CharField(
        _("action"),
        max_length=5,
        choices=SignalAction.choices,
        default=SignalAction.BUY,
        help_text=_("The action of the signal."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of the signal."),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this signal is active."),
    )
    targets = ArrayField(
        models.FloatField(),
        help_text="Profit targets",
        null=True,
        blank=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name=_("author"),
        on_delete=models.CASCADE,
        related_name="signals",
    )

    def __str__(self):
        return f"{self.term} {self.action} signal at {self.entry}"
