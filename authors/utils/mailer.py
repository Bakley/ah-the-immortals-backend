from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


class VerificationMail:
    """
    Email class for sending verification mail
    """

    def __init__(self, user, token):
        self.user = user
        self.token = token
        self.message = None

    def compose_mail(self):
        """
        Composes the email
        """
        html_body = render_to_string(
            template_name="password_reset.html",
            context={
                "name": self.user.username,
                "action_url": settings.PASSWORD_RESET_URL_PREFIX+self.token.key
            }
        )
        self.message = EmailMultiAlternatives(
            subject="Password Reset",
            body="This is a mail to reset your password",
            from_email=settings.DEFAULT_EMAIL,
            to=[self.user.email]
        )
        self.message.attach_alternative(html_body, "text/html")

    def send_mail(self):
        """
        Sends the composed email
        """
        self.compose_mail()
        self.message.send()


class ConfirmationMail:
    """
    Email class for sending confirmation mail
    """

    def __init__(self, data):
        self.username = data.get("username")
        self.email = data.get("email")
        self.token = data.get("token")

    def compose_mail(self):
        """
        Composes the email
        """
        html_body = render_to_string(
            template_name="mail.html",
            context={
                "name": self.username,
                "verification": settings.VERIFICATION_URL+self.token
            }
        )
        self.message = EmailMultiAlternatives(
            subject="Welcome {}".format(self.username),
            body="Confirmation email",
            from_email=settings.DEFAULT_EMAIL,
            to=[self.email]
        )
        self.message.attach_alternative(html_body, "text/html")

    def send_mail(self):
        """
        Sends the composed email
        """
        self.compose_mail()
        self.message.send()
