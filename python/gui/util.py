from base64 import b64encode, b64decode
from Crypto.Cipher import AES

LABEL_SORT = {
    'address': 0,
    'port': 1,
    'username': 2,
    'password': 3,
    'protocol': 4,
    'mailbox': 5
}

GET_DEFAULT = {
    'sys': {
        'address': '127.0.0.1',
        'port': '10086',
        'username': 'admin',
        'password': 'my_password',
    },
    'email': {
        'address': 'imap.example.com',
        'username': 'my_account@example.com',
        'password': 'my_password',
        'protocol': 'imap',
        'mailbox': 'INBOX',
    }
}


class Result(object):
    def __init__(self, action='', result=False, msg=''):
        self.action = action
        self.result = result
        self.msg = msg


class AESCipher:
    def __init__(self, secretkey: str):
        self.key = secretkey.encode()
        self.iv = secretkey[0: AES.block_size].encode()
        self.block_size = AES.block_size

    def pad(self, s):
        return s + (self.block_size - len(s.encode()) % self.block_size) * chr(
            self.block_size - len(s.encode()) % self.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def encrypt(self, text):
        text = self.pad(text).encode()
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv)
        encrypted_text = cipher.encrypt(text)
        return b64encode(encrypted_text).decode('utf-8')

    def decrypt(self, encrypted_text):
        encrypted_text = b64decode(encrypted_text)
        cipher = AES.new(key=self.key, mode=AES.MODE_CBC, IV=self.iv)
        decrypted_text = cipher.decrypt(encrypted_text)
        return self.unpad(decrypted_text).decode('utf-8')


if __name__ == '__main__':
    pass
