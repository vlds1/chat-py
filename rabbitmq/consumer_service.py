import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Sequence, Union

from aio_pika import IncomingMessage
from config import get_config
from logger.logger_config import get_logger


class EmailService:
    def __init__(self):
        self.config = get_config()
        self.logger = get_logger()

    async def send_mail(self, message: IncomingMessage) -> None:
        receiver = message.headers["to_user"]
        server = await self.get_server()
        try:
            msg = await self.set_msg(self.config.EMAIL_SENDER, receiver, message)
            server.sendmail(self.config.EMAIL_SENDER, receiver, msg.as_string())
            server.quit()
            self.logger.info("[rabbit_consumer] message sent to email successfully")
        except Exception as e:
            self.logger.error(f"[rabbit_consumer: send_message] {e}")

    async def set_msg(
        self, sender: str, receiver: Union[str, Sequence[str]], message: IncomingMessage
    ) -> MIMEMultipart:
        msg = MIMEMultipart()
        user = message.headers["from_user"]
        decoded_message = message.body.decode("utf-8")
        msg["From"] = f"Chat <{sender}>"
        msg["To"] = receiver
        msg["Subject"] = "New message"
        text = f"New message by {user!r}: {decoded_message!r}"
        part = MIMEText(text, "plain")
        msg.attach(part)
        return msg

    async def get_server(self) -> smtplib.SMTP:
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(self.config.EMAIL_SENDER, self.config.EMAIL_PASSWORD)
            self.logger.info(
                "[rabbit_consumer: get_server] successfully connected to SMTP server"
            )
            return server
        except Exception as e:
            self.logger.error(f"[rabbit_consumer: get_server] {e}")
            raise Exception
