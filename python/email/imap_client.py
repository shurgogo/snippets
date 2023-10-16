import imaplib
import email
from email.header import decode_header

def fetch_imap(self):
    self.imap.select('TEST2023', readonly=True)
    # Search for emails
    search_criteria = '(UNSEEN)'  # You can modify this criteria
    status, email_ids = self.imap.search(None, search_criteria)

    # List to store email messages
    emails = []
    if status == 'OK':
        print(status)
        email_id_list = email_ids[0].split()
        for email_id in email_id_list:
            status, msg_data = self.imap.fetch(email_id, '(RFC822)')  # Fetch the email message
            if status == 'OK':
                email_msg = email.message_from_bytes(msg_data[0][1])
                subject, encoding = decode_header(email_msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding is not None else 'utf-8')
                from_ = email_msg.get("From")
                date = email_msg.get("Date")
                body = ""

                if email_msg.is_multipart():
                    for part in email_msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()

                emails.append({"subject": subject, "from": from_, "date": date, "body": body})
                return emails
    return emails

if __name__ == '__main__':
    # Connect to the IMAP server
    server = imaplib.IMAP4('127.0.0.1', port=14300)  # Make sure to use the correct hostname and port

    # Log in
    server.login('username', 'password')  # Use appropriate username and password

    # Select mailbox
    server.select('inbox')

    # Fetch email
    response, data = server.fetch('1', '(BODY[TEXT])')
    print(data[0][1].decode())

    # Logout
    server.logout()
