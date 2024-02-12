import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from zedasignal_backend.apps.users.managers import CustomUserManager
from zedasignal_backend.core.mixins import CreatedAndUpdatedAtMixin, CreatedAtMixin
from zedasignal_backend.core.utils.main import generate_numeric_code


class User(AbstractUser):
    """
    Default custom user model for Zedasignal Backend.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    email = models.EmailField(_("email address"), unique=True, blank=True, null=True)
    phone_number = models.CharField(
        _("phone number"), blank=True, null=True, max_length=20
    )

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    # use a better name for custom user manager
    user_manager = CustomUserManager()

    def __str__(self):
        return self.username

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


# create user profile model
class Profile(CreatedAndUpdatedAtMixin, models.Model):
    """
    User profile model for Zedasignal Backend.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        on_delete=models.CASCADE,
        related_name="profile",
    )
    has_trading_experience = models.BooleanField(
        _("has trading experience"),
        default=False,
        help_text=_("Designates whether this user has trading experience."),
    )
    ref_id = models.CharField(
        _("referral id"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The referral id of this user."),
    )
    amount_range_to_trade_with = models.CharField(
        _("amount range to trade with"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The amount range to trade with."),
    )
    uuid = models.UUIDField(
        _("uuid"),
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text=_("Unique identifier for this user profile."),
    )

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")


class VerificationCode(CreatedAtMixin, models.Model):
    """
    Verification code model for Zedasignal Backend.
    """

    code = models.CharField(_("code"), max_length=6)
    used = models.BooleanField(_("used"), default=False)
    email = models.EmailField(
        _("email"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The email to which the code was sent."),
    )

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = _("verification code")
        verbose_name_plural = _("verification codes")
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """
        Override the save method to generate a numeric code.
        """
        if not self.code:
            self.code = generate_numeric_code(6)
        super().save(*args, **kwargs)
