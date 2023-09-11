import smtplib
import imaplib
from email.mime.text import MIMEText
from email.parser import BytesParser



class MailClient:
    def __init__(self, pop3_server, username, password):
        self.pop3_server = pop3_server
        self.username = username
        self.password = password

    def list_emails(self):
        with imaplib.IMAP4(self.pop3_server) as server:
            server.login(self.username, self.password)
            server.select("inbox")
            _, data = server.search(None, "ALL")
            email_ids = data[0].split()
            emails = []
            for email_id in email_ids:
                _, msg_data = server.fetch(email_id, "(RFC822)")
                msg = BytesParser().parsebytes(msg_data[0][1])
                emails.append(msg)
            return emails


if __name__ == "__main__":
    pop3_server_addr = "0.0.0.0"
    username = "author@example.com"
    password = "your_password"

    client = MailClient(pop3_server_addr, username, password)

    client.list_emails()

