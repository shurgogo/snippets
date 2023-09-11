import imaplib

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
