from importlib import import_module

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from zedasignal_backend.core.termii.termii import Termii


class Sender:
    def __init__(
        self,
        user_account,
        *,
        email_content_object=None,
        notification=None,
        context=None,
        email_notif=False,
        sms_notif=False,
        push_notif=False,
        html_template=None,
        sms_message=None,
        device=None,
        notification_type=None,
        text=None,
        data=None,
        title=None,
        **kwargs,
    ):
        self.user_account = user_account
        self.email_content_object = email_content_object
        self.notification = notification
        self.html_template = html_template
        self.context = context
        self.email_notif = email_notif
        self.sms_notif = sms_notif
        self.push_notif = push_notif
        self.sms_message = sms_message if sms_message is not None else "New Message"
        self.device = device
        self.notification_type = notification_type
        self.text = text
        self.data = data
        self.title = title

        self.send()

    def email(self):
        """
        Sends an email to the affected party and
        """

        # dynamic file import module and object construction
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
        email_content_object = render_to_string(self.template_name, context=context)
        msg = EmailMultiAlternatives(
            subject,
            email_content_object,
            self.email_from,
            [self.user_account.email],
        )
        msg.content_subtype = "html"
        msg.send(fail_silently=False)

        return "Mail sent"

    def sms(self):
        termii = Termii()
        termii.send_sms(to=self.user_account.phone_number, message=self.sms_message)
        return "SMS sent"

    def push(self):
        pass

    def send(self):
        if self.email_notif:
            return self.email()

        if self.sms_notif:
            return self.sms()

        if self.push_notif:
            return self.push()
