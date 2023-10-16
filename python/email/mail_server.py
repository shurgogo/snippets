import smtpd
import asyncore
from email.parser import BytesParser
from email.mime.text import MIMEText

mailbox = []

class CustomSMTPServer(smtpd.SMTPServer):
    def __init__(self, localaddr, remoteaddr):
        super().__init__(localaddr, remoteaddr)

    def process_message(self, peer, mailfrom, rcpttos, data, **my_krargs):
        print('Receiving message from:', peer)
        print('Message addressed from:', mailfrom)
        print('Message addressed to:', rcpttos)
        print('Message length:', len(data))
        try:
            msg = BytesParser().parsebytes(data)
            mailbox.append(msg)
            print("Received a new email:", msg['subject'])
        except Exception as e:
            print(e.args)


class CustomPOP3Server(asyncore.dispatcher):
    def __init__(self, localaddr):
        super().__init__()
        self.create_socket()
        self.bind(localaddr)
        self.listen(5)

    def handle_accept(self):
        client, addr = self.accept()
        CustomPOP3Handler(client, mailbox)


class CustomPOP3Handler(asyncore.dispatcher):
    def __init__(self, client, mailbox):
        super().__init__(client)
        self.mailbox = mailbox
        self.buffer = b"+OK POP3 server ready\r\n"

    def handle_read(self):
        command = self.recv(1024).decode().strip()
        if command == "LIST":
            response = "+OK\r\n"
            for i, _ in enumerate(self.mailbox, start=1):
                response += f"{i} {i}\r\n"
            response += ".\r\n"
            self.buffer = response.encode()
        elif command.startswith("RETR"):
            index = int(command.split()[1]) - 1
            if 0 <= index < len(self.mailbox):
                email = self.mailbox[index]
                self.buffer = email.as_string().encode()
            else:
                self.buffer = b"-ERR Invalid index\r\n"
        elif command == "QUIT":
            self.buffer = b"+OK POP3 server signing off\r\n"
            self.close()
        else:
            self.buffer = b"-ERR Command not recognized\r\n"
        self.send(self.buffer)
        self.buffer = b""


if __name__ == "__main__":
    smtp_server = CustomSMTPServer(('127.0.0.1', 1025), None)
    # pop3_server = CustomPOP3Server(('0.0.0.0', 110))

    asyncore.loop()
