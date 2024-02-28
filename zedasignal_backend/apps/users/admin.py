from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import decorators, get_user_model

from zedasignal_backend.apps.users import models
from zedasignal_backend.apps.users.forms import UserAdminChangeForm, UserAdminCreationForm

# from django.utils.translation import gettext_lazy as _


User = get_user_model()

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://django-allauth.readthedocs.io/en/stable/advanced.html#admin
    admin.site.login = decorators.login_required(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class CustomUserAdmin(auth_admin.UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone_number",
        "is_active",
    )
    ordering = ["-date_joined"]
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    search_fields = ["email", "first_name", "last_name"]
    fieldsets = auth_admin.UserAdmin.fieldsets + (
        (
            "Other Information",
            {
                "fields": (
                    "phone_number",
                    "nickname",
                    "type",
                )
            },
        ),  # type: ignore
        # (
        #     _("Permissions"),
        #     {
        #         "fields": (
        #             "is_active",
        #             "is_superuser",
        #             "groups",
        #             "user_permissions",
        #         ),
        #     },
        # ),
        # (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )


@admin.register(models.VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "code",
        "used",
    )
    readonly_fields = ("code", "created_at")


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "has_trading_experience",
        "ref_id",
        "amount_range_to_trade_with",
    )
    readonly_fields = ("uuid",)
    ordering = ["-created_at"]
