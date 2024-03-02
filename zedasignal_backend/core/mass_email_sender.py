from importlib import import_module
from typing import Any

from core.utils import send_mass_html_mail
from django.core.mail import EmailMultiAlternatives
from django.db.models import QuerySet
from django.template.loader import render_to_string

from zedasignal_backend.apps.users.utils import get_custom_user_model

User = get_custom_user_model()


class MassEmailSender:
    def __init__(
        self,
        users: QuerySet[User] | list[User],
        html_template: str,
        email_content_object=None,
        include_user_in_context=False,
        context=None,
    ):
        self.users = users
        self.email_content_object = email_content_object
        self.html_template = html_template
        self.include_user_in_context = include_user_in_context
        self.email_messages_for_users: list[EmailMultiAlternatives] = []

        self.context: dict[str, Any] = {} if context is None else context

        self.setup_user_for_mass_emails()
        self.send_mass_emails_to_users()

    def send_mass_emails_to_users(self):
        number_of_delivered_emails = send_mass_html_mail(self.email_messages_for_users, fail_silently=False)
        return f"Number of delivered emails {number_of_delivered_emails}"

    def setup_user_for_mass_emails(self):
        assert self.email_content_object is not None, "Email content object is required"
        file = import_module(self.email_content_object).MyMessages

        self.email_subject = str(file.EMAIL_SUBJECT) if file.EMAIL_SUBJECT else "New Message"
        self.email_from = (
            str(file.FROM_ADDRESS)
            if getattr(file, "FROM_ADDRESS", None)
            else "Zedasignal Notifier <noreply@zedasignal.com>"
        )

        self.email_message = None if not hasattr(file, "EMAIL_MESSAGE") else file.EMAIL_MESSAGE

        self.template_name = self.html_template if self.html_template else "email/base.html"

        subject = self.email_subject
        context = (
            self.context
            if self.context
            else {
                "subject": subject,
                "body": self.email_message,
            }
        )
        if not self.include_user_in_context:
            email_content_object = render_to_string(self.template_name, context=context)
            for user in self.users:
                email_message = EmailMultiAlternatives(
                    subject,
                    email_content_object,
                    self.email_from,
                    [user.username],
                )
                email_message.content_subtype = "html"
                self.email_messages_for_users.append(email_message)
        else:
            for user in self.users:
                context["user"] = user
                email_content_object = render_to_string(self.template_name, context=context)
                email_message = EmailMultiAlternatives(
                    subject,
                    email_content_object,
                    self.email_from,
                    [user.username],
                )
                email_message.content_subtype = "html"
                self.email_messages_for_users.append(email_message)
