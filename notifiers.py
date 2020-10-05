import os
import smtplib
from email.message import EmailMessage
from abc import ABC, abstractmethod

from dotenv import load_dotenv
load_dotenv()


class Notifier(ABC):

    @abstractmethod
    def notify(self):
        pass


class EmailNotifier(Notifier):

    def __init__(self):
        self.host = os.getenv("EMAIL_HOST")
        self.port = os.getenv("EMAIL_PORT")
        self.username = os.getenv("EMAIL_HOST_USER")
        self.password = os.getenv("EMAIL_HOST_PASSWORD")

    def _create_connection(self):
        self.connection = smtplib.SMTP(self.host, self.port)

    def _close_connection(self):
        self.connection.close()

    def _login(self):
        self.connection.ehlo()
        self.connection.starttls()
        self.connection.ehlo()

        self.connection.login(self.username, self.password)

    def _prepare_content(self, subject, content, recipients):
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = ", ".join(recipients)
        msg.set_content(content)

        self.msg = msg

    def notify(self, subject, content, recipients):
        self._create_connection()

        if self.username and self.password:
            self._login()

        self._prepare_content(subject, content, recipients)

        self.connection.send_message(self.msg)

        self._close_connection()


class SlackNotifier(Notifier):

    def __init__(self):
        pass

    def notify(self):
        print("I am notifying via Slack")


class SMSNotifier(Notifier):

    def __init__(self):
        pass

    def notify(self):
        print("I am notifying via SMS")
