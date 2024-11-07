from base64 import b64decode, b64encode

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


class Vault:
    magic = "$Vault"
    separator = ";"

    def __init__(self, passkey: bytes):
        self.passkey = passkey

    def encrypt(self, payload: str) -> str:
        nonce = get_random_bytes(12)
        cipher = AES.new(self.passkey, AES.MODE_GCM, nonce=nonce)
        data, tag = cipher.encrypt_and_digest(payload.encode("utf-8"))
        return self.separator.join([
            self.magic,
            b64encode(nonce).decode("utf-8"),
            b64encode(data).decode("utf-8"),
            b64encode(tag).decode("utf-8")])

    def decrypt(self, payload: str) -> str:
        magic, nonce, data, tag, *_meta = payload.split(self.separator)
        if magic == self.magic and nonce and data:
            cipher = AES.new(self.passkey, AES.MODE_GCM,
                             nonce=b64decode(nonce))
            return cipher.decrypt_and_verify(
                b64decode(data), b64decode(tag)).decode("utf-8")
        raise RuntimeError("Couldn't decrypt payload")

    @staticmethod
    def prefix():
        return f"{Vault.magic}{Vault.separator}"
