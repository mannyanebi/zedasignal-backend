from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce import HTMLField
from zedasignal_backend.apps.users.types import UserType
from zedasignal_backend.core.mixins import CreatedAndUpdatedAtMixin, UUIDMixin


# Create your models here.
class Bot(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    Bots model for Zedasignal Backend.
    Stores information and links for bots.
    """

    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of this bot."),
    )
    min_investment_amount = models.CharField(
        _("min investment amount"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The min investment amount of this bot."),
    )
    max_investment_amount = models.CharField(
        _("max investment amount"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The max investment amount of this bot."),
    )
    performance_fee = models.CharField(
        _("performance fee"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The performance fee of this bot."),
    )
    overall = models.CharField(
        _("overall"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The overall of this bot."),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this bot is active."),
    )
    is_top_performing = models.BooleanField(
        _("is top performing"),
        default=False,
        help_text=_("Designates whether this bot is top performing."),
    )

    def __str__(self):
        return self.name


class TopPerformingBot(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    TopPerformingBots model for Zedasignal Backend.
    Stores information and links for top performing bots.
    """

    bot = models.ForeignKey(
        Bot,
        verbose_name=_("bot"),
        on_delete=models.CASCADE,
        related_name="top_performing_bots",
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of this top performing bot."),
    )
    price = models.CharField(
        _("price"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The price of this top performing bot."),
    )
    period = models.CharField(
        _("period"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The period of this top performing bot."),
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.bot.name


class SubscriptionPlanPromo(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    SubscriptionPlanPromo model for Zedasignal Backend.
    Stores information and links for subscription plan promos.
    """

    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of this subscription plan promo."),
    )

    def __str__(self):
        return self.name


class SubscriptionPlan(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    SubscriptionPlan model for Zedasignal Backend.
    Stores information and links for subscription plans.
    """

    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of this subscription plan."),
    )
    yearly_price = models.CharField(
        _("yearly price"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The yearly price of this subscription plan."),
    )
    description = models.TextField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of this subscription plan."),
    )
    is_active = models.BooleanField(
        _("is active"),
        default=True,
        help_text=_("Designates whether this subscription plan is active."),
    )
    is_special = models.BooleanField(
        _("is special"),
        default=False,
        help_text=_("Designates whether this subscription plan is special."),
    )
    button_cta = models.CharField(
        _("button cta"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The button cta of this subscription plan."),
    )
    promos = models.ManyToManyField(
        SubscriptionPlanPromo,
        verbose_name=_("promos"),
        blank=True,
        help_text=_("The promos of this subscription plan."),
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["created_at"]


class AccountScreeningRequest(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    AccountScreeningRequest model for Zedasignal Backend.
    Stores information and links for account screening requests.
    """

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="account_screening_requests",
    )
    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of the user requesting for account screening."),
    )
    email = models.EmailField(
        _("email"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The email of the user requesting for account screening."),
    )
    phone_number = models.CharField(
        _("phone number"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The phone number of the user requesting for account screening."),
    )
    schedule_date = models.DateField(
        _("schedule date"),
        blank=True,
        null=True,
        help_text=_("The schedule date of the user requesting for account screening."),
    )
    schedule_time = models.TimeField(
        _("schedule time"),
        blank=True,
        null=True,
        help_text=_("The schedule time of the user requesting for account screening."),
    )
    is_approved = models.BooleanField(
        _("is approved"),
        default=False,
        help_text=_("Designates whether this account screening request is approved."),
    )
    country = models.CharField(
        _("country"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The country of the user requesting for account screening."),
    )
    trading_capital_amount = models.CharField(
        _("trading capital amount"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "The trading capital amount of the user requesting for account screening."
        ),
    )
    has_trading_experience = models.BooleanField(
        _("has trading experience"),
        default=False,
        help_text=_(
            "Designates whether the user requesting for account screening has trading experience."
        ),
    )
    previously_used_forex_broker = models.CharField(
        _("previously used forex broker"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "The previously used forex broker of the user requesting for account screening."
        ),
    )

    def __str__(self):
        return str(self.user)

    class Meta:
        ordering = ["-created_at"]


class CopyTradingGuide(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    CopyTradingGuide model for Zedasignal Backend.
    Stores information and links for copy trading guides.
    """

    bot = models.ForeignKey(
        Bot,
        verbose_name=_("bot"),
        on_delete=models.CASCADE,
        related_name="copy_trading_guides",
    )
    description = HTMLField(
        _("description"),
        blank=True,
        null=True,
        help_text=_("The description of this copy trading guide."),
    )

    def __str__(self):
        return self.bot.name


class BotlabBot(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    name = models.CharField(
        _("name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of this bot."),
    )
    name_of_broker = models.CharField(
        _("name of broker"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The name of broker of this bot."),
    )
    server_name = models.CharField(
        _("server name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The server name of this bot."),
    )
    investor_login = models.CharField(
        _("investor login"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The investor login of this bot."),
    )
    investor_password = models.CharField(
        _("investor password"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The investor password of this bot."),
    )
    terminal = models.CharField(
        _("terminal"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The terminal of this bot."),
    )
    test_commencement_date = models.DateField(
        _("test commencement date"),
        blank=True,
        null=True,
        help_text=_("The test commencement date of this bot."),
    )
    is_delisted = models.BooleanField(
        _("is delisted"),
        default=False,
        help_text=_("Designates whether this bot is delisted."),
    )

    def __str__(self):
        return self.name


class AccountUpgradePaymentRequest(UUIDMixin, CreatedAndUpdatedAtMixin, models.Model):
    """
    AccountUpgradePaymentRequest model for Zedasignal Backend.
    Stores information and links for account upgrade payment requests.
    """

    user = models.ForeignKey(
        "users.User",
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="account_upgrade_payment_requests",
    )
    subscription_plan = models.ForeignKey(
        SubscriptionPlan,
        verbose_name=_("subscription plan"),
        on_delete=models.CASCADE,
        related_name="account_upgrade_payment_requests",
    )

    user: models.ForeignKey[UserType]

    def __str__(self):
        return str(self.user)
