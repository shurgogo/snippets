import smtplib
from email.mime.text import MIMEText


class MailClient:
    def __init__(self, smtp_server_addr, username, password):
        self.smtp_server_addr = smtp_server_addr
        self.username = username
        self.password = password

    def send_email(self, to_addr, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.username
        msg['To'] = to_addr

        with smtplib.SMTP(self.smtp_server_addr, 1025) as server:
            server.set_debuglevel(True)
            server.sendmail(
                from_addr=self.username,
                to_addrs=[to_addr],
                msg=msg.as_string()
            )


if __name__ == "__main__":
    smtp_server_addr = "127.0.0.1"
    username = "author@example.com"
    password = "your_password"

    client = MailClient(smtp_server_addr, username, password)

    client.send_email(
        'recipient@example.com',
        'Simple test message',
        'This is the body of the message.'
    )

