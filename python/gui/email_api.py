import imaplib
import poplib
import email
from email.header import decode_header
import logging


class EmailClient(object):
    def __init__(self, addr, user, passwd):
        self._addr = addr
        self._user = user
        self._passwd = passwd

    def login(self) -> bool:
        return False

    def fetch(self):
        return []

    def close(self):
        pass


class IMAPClient(EmailClient):
    def __init__(self, addr, user, passwd, mailbox='INBOX'):
        super().__init__(addr, user, passwd)
        self._client = None
        self._mailbox = mailbox

    def login(self) -> bool:
        try:
            self._client = imaplib.IMAP4_SSL(self._addr)
            self._client.login(self._user, self._passwd)
            logging.info('login imap server success')
            return True
        except Exception as e:
            logging.error('login imap server failed: %s' % e.args)
            return False

    def fetch(self):
        # select a mailbox
        self._client.select(self._mailbox, readonly=True)
        # search ALL emails
        status, email_ids = self._client.search(None, 'ALL')

        if status != 'OK':
            logging.error('imap search failed: status is %s' % status)
            return []
        emails = []
        # list to store email messages
        email_id_list = email_ids[0].split()
        for email_id in email_id_list:
            # fetch the email by ID
            status, msg_data = self._client.fetch(email_id, '(RFC822)')
            if status != 'OK':
                continue
            # parse the email content
            e = _create_email_from_bytes_msg(msg_data[0][1])
            emails.append(e)
        return emails

    def close(self):
        self._client.logout()


class POP3Client(EmailClient):
    def __init__(self, addr, user, passwd, mailbox='INBOX'):
        super().__init__(addr, user, passwd)
        self._client = None
        self._mailbox = mailbox

    def login(self) -> bool:
        try:
            self._client = poplib.POP3_SSL(self._addr)
            self._client.user(self._user)
            self._client.pass_(self._passwd)
            logging.info('login pop3 server success')
            return True
        except Exception as e:
            logging.error('login pop3 server failed: %s' % e.args)
            return False

    def fetch(self):
        # Get the total number of emails in the mailbox
        msg_count = len(self._client.list()[1])
        # List to store email messages
        emails = []
        for i in range(msg_count):
            # response, content lines, content byte size
            _, lines, _ = self._client.retr(i + 1)
            # join lines to a content
            msg_bytes_content = b'\r\n'.join(lines)
            # parse bytes msg
            e = _create_email_from_bytes_msg(msg_bytes_content)
            emails.append(e)
        return emails

    def close(self):
        self._client.quit()


class FakeEmailClient(EmailClient):
    def __init__(self, addr, user, passwd, mailbox=''):
        self._addr = addr
        self._user = user
        self._passwd = passwd

    def login(self) -> bool:
        return True

    def fetch(self):
        return []

    def close(self):
        pass


def _create_email_from_bytes_msg(bytes_msg: bytes):
    # parse msg
    msg = email.message_from_bytes(bytes_msg)
    # get title
    title, encoding = decode_header(msg['Subject'])[0]
    if isinstance(title, bytes):
        title = title.decode(encoding if encoding else 'utf-8')
    # get from
    from_, encoding = decode_header(msg['From'])[0]
    if isinstance(from_, bytes):
        from_ = from_.decode(encoding if encoding else 'utf-8')
    # get date
    date = msg.get('Date')
    # get content
    content = ''
    if msg.is_multipart():
        content = msg.get_payload(decode=True)
        charset = guess_charset(msg)
        if charset:
            content = content.decode(charset)

    return {
        'Title': title,
        'From': from_,
        'Date': date,
        'Content': content
    }


def guess_charset(msg):  # 获取邮件编码
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


if __name__ == '__main__':
    pop3 = POP3Client('pop.sina.com', 'myemail@sina.com', 'passwd')
    login_success = pop3.login()
    if not login_success:
        exit(-1)
    es = pop3.fetch()
    pop3.close()
    print(es)
    # imap = IMAPClient('imap.sina.com', 'myemail@sina.com', 'passwd', 'INBOX')
    # login_success = imap.login()
    # if not login_success:
    #     exit(-1)
    # es = imap.fetch()
    # imap.close()
    # print(es)
