from base64 import b64encode, b64decode
from Crypto.Cipher import AES


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
    key = '1234123412341234abcdabcdabcdabcd'
    cipher = AESCipher('1234123412341234abcdabcdabcdabcd')
    print(cipher.encrypt('hefasdfllo'))
    print(cipher.decrypt('IplZWmc4fx4hw84H/oLqyA=='))
