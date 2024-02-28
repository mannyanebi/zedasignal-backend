from django.db import models
from django.utils.translation import gettext_lazy as _
from django_jsonform.models.fields import ArrayField
from djmoney.models.fields import MoneyField

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

    id: int
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
    pair_base = models.CharField(
        _("pair base"),
        max_length=10,
        blank=False,
        null=False,
        help_text=_("The base pair of the signal."),
    )
    pair_quote = models.CharField(
        _("pair quote"),
        max_length=10,
        blank=False,
        null=False,
        help_text=_("The quote pair of the signal."),
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


class SubscriptionPlan(CreatedAndUpdatedAtMixin, UUIDMixin, models.Model):
    """
    Subscription Plan model for Zedasignal Backend.
    """

    TELEGRAM = "telegram"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    SMS = "sms"

    class NotificationChannels(models.TextChoices):
        TELEGRAM = "telegram", "Telegram"
        WHATSAPP = "whatsapp", "WhatsApp"
        EMAIL = "email", "Email"
        SMS = "sms", "SMS"

    id: int
    name = models.CharField(
        _("name"),
        max_length=255,
        blank=False,
        null=False,
        help_text=_("The name of the subscription plan."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of the subscription plan."),
    )
    monthly_price = MoneyField(
        _("monthly price"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        help_text=_("The price of the subscription plan per month"),
    )  # type: ignore
    yearly_price = MoneyField(
        _("yearly price"),
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        help_text=_("The price of the subscription plan per year"),
    )  # type: ignore
    notification_channels = ArrayField(
        models.CharField(
            max_length=10,
            choices=NotificationChannels.choices,
            default=NotificationChannels.TELEGRAM,
        ),
        help_text="Notification channels, choices are telegram, whatsapp, email, sms.",
        null=False,
        blank=False,
    )
    benefits = ArrayField(
        models.CharField(max_length=255),
        help_text="Benefits",
        null=True,
        blank=True,
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this subscription plan is active."),
    )
    creator = models.ForeignKey(
        User,
        verbose_name=_("creator"),
        on_delete=models.CASCADE,
        related_name="subscription_plans_created",
    )

    def __str__(self):
        return self.name


class Subscription(CreatedAndUpdatedAtMixin, UUIDMixin, models.Model):
    """
    Subscription model for Zedasignal Backend.
    """

    id: int
    user = models.ForeignKey(
        User,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        verbose_name=_("plan"),
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    start_timestamp = models.DateTimeField(
        _("start date"),
        blank=False,
        null=False,
        help_text=_("The start date of the subscription."),
    )
    end_timestamp = models.DateTimeField(
        _("end date"),
        blank=False,
        null=False,
        help_text=_("The end date of the subscription."),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this subscription is active."),
    )

    def __str__(self):
        return f"{self.user} - {self.plan}"
