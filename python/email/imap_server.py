import socket


class IMAPServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.mailboxes = {
            'inbox': [
                {'seq': 1, 'flags': ['\\Seen'], 'body': 'Hello, world!', 'date': '27-Aug-2023'}
            ]
        }
        self.selected_mailbox = None

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()

            print(f"Server listening on {self.host}:{self.port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Connection from {client_address}")
                self.handle_client(client_socket)

    def handle_client(self, client_socket):
        client_socket.send(b"* OK IMAP server ready\r\n")

        while True:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                break

            command = data.split(' ')[0].upper()

            if command == 'CAPABILITY':
                client_socket.send(b"* CAPABILITY IMAP4rev1\r\n")
                client_socket.send(b"A01 OK CAPABILITY completed\r\n")
            elif command == 'LOGIN':
                client_socket.send(b"A02 OK LOGIN completed\r\n")
            elif command == 'SELECT':
                mailbox_name = data.split(' ')[-1][1:-1]
                if mailbox_name in self.mailboxes:
                    self.selected_mailbox = mailbox_name
                    client_socket.send(b"A03 OK SELECT completed\r\n")
                else:
                    client_socket.send(b"A03 NO Mailbox not found\r\n")
            elif command == 'FETCH':
                if self.selected_mailbox:
                    email_data = self.mailboxes[self.selected_mailbox][0]['body']
                    response = f"* 1 FETCH (BODY[TEXT] {{13}}\r\n{email_data})\r\n"
                    client_socket.send(response.encode())
                    client_socket.send(b"A04 OK FETCH completed\r\n")
                else:
                    client_socket.send(b"A04 NO No mailbox selected\r\n")
            else:
                client_socket.send(b"BAD Unknown command\r\n")

        client_socket.close()


if __name__ == "__main__":
    server = IMAPServer('localhost', 14300)  # Adjust host and port as needed
    server.start()
