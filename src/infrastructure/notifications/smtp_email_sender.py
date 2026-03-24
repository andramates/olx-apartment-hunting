import smtplib
from email.message import EmailMessage

from src.application.ports.email_sender import EmailSender
from src.infrastructure.config.settings import get_settings


class SmtpEmailSender(EmailSender):
    def __init__(self):
        self.settings = get_settings()

    def send(self, to_email: str, subject: str, body: str) -> None:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.settings.smtp_from
        msg["To"] = to_email
        msg.set_content(body)

        with smtplib.SMTP(self.settings.smtp_host, self.settings.smtp_port) as smtp:
            smtp.starttls()
            smtp.login(self.settings.smtp_user, self.settings.smtp_password)
            smtp.send_message(msg)