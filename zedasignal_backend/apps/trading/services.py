from typing import Literal

import environ
from django.db.models.query import QuerySet

from zedasignal_backend.apps.trading.models import Signal, Subscription
from zedasignal_backend.apps.users.utils import get_custom_user_model
from zedasignal_backend.core.mass_email_sender import MassEmailSender
from zedasignal_backend.core.sender import Sender

User = get_custom_user_model()
env = environ.Env()

channels_type = Literal["email", "sms", "whatsapp", "telegram"]


class SignalService:
    @staticmethod
    def fetch_active_subscriptions_grouped_by_channels():
        """
        This method fetches all active subscriptions. Groups by subscription channels_type and returns a dictionary of
        subscription channels_type and their respective subscribers.
        """
        active_subscriptions = Subscription.objects.select_related("user").filter(is_active=True, user__is_active=True)

        active_subscriptions_by_channels: dict[channels_type, list[User]] = {}
        for subscription in active_subscriptions:
            all_channels = list(subscription.plan.notification_channels)  # type: ignore
            for channel in all_channels:
                if channel not in active_subscriptions_by_channels:
                    active_subscriptions_by_channels[channel] = []
                active_subscriptions_by_channels[channel].append(subscription.user)

        return active_subscriptions_by_channels

    @staticmethod
    def fetch_active_subscriptions_users_by_channel(channel: channels_type):
        """
        This method fetches all active subscriptions by channel.

        Args:
            channel (channels_type): The channel to fetch active subscriptions for.
        """
        active_subscriptions = Subscription.objects.select_related("user").filter(
            is_active=True,
            user__is_active=True,
            plan__notification_channels__contains=[channel],
        )

        user_ids = active_subscriptions.values_list("user", flat=True)
        return User.objects.filter(id__in=user_ids)

    @staticmethod
    def send_signal_to_subscriber(signal: Signal, user: User):
        """
        This method sends a signal to a subscriber.

        Args:
            signal (Signal): The signal to be sent.
            user (User): The user to send the signal to.
        """
        domain = env.str("DOMAIN_NAME")
        Sender(
            user,
            email_content_object="notification.messages.signals",
            html_template="emails/trading/signals/notification.html",
            email_notif=True,
            context={"signal": signal, "user": user, "domain": domain},
        )

    @staticmethod
    def send_signal_to_subscribers_by_email(signal: Signal, users: list[User] | QuerySet[User]):
        """
        This method sends a signal to subscribers by email.

        Args:
            signal (Signal): The signal to be sent.
            users (List[User] | QuerySet[User]): The list of users to send the signal to.
        """
        domain = env.str("DOMAIN_NAME")
        MassEmailSender(
            users=users,
            email_content_object="notification.messages.signals",
            html_template="emails/trading/signals/notification.html",
            include_user_in_context=True,
            context={"signal": signal, "domain": domain},
        )

    @staticmethod
    def send_signal_to_subscribers_by_sms(signal: Signal, users: list[User] | QuerySet[User]):
        """
        This method sends a signal to subscribers by sms.

        Args:
            signal (Signal): The signal to be sent.
            users (List[User] | QuerySet[User]): The list of users to send the signal to.
        """
        pass

    @staticmethod
    def publish_signal_to_active_subscribers_by_email(signal: Signal):
        """
        This method publishes a signal to active subscribers by email.

        Args:
            signal (Signal): The signal to be published.
            channel (channels_type): The channel to publish the signal to.
        """
        users = SignalService.fetch_active_subscriptions_users_by_channel("email")

        SignalService.send_signal_to_subscribers_by_email(signal, users)

    @staticmethod
    def publish_signal_to_active_subscribers_by_sms(signal: Signal):
        """
        This method publishes a signal to active subscribers by sms.

        Args:
            signal (Signal): The signal to be published.
        """
        users = SignalService.fetch_active_subscriptions_users_by_channel("sms")

        # for user in users:
