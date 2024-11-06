import base64
import os

from cryptography import fernet
from cryptography.hazmat import backends
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf import pbkdf2

__all__ = [
    "FernetBinaryFieldData",
    "FernetTextFieldData",
]


class FernetBinaryFieldData:
    ITERATIONS = 100000

    def __init__(self, raw=None, base64_str=None):
        if raw is not None and base64_str is not None:
            raise ValueError("cannot set both 'raw' and 'base64_str'")

        if base64_str:
            raw = base64.b64decode(base64_str.encode("ASCII"))

        if raw and len(raw) >= 16:
            self._salt = raw[:16]
            self._data = raw[16:]

        else:
            self._salt = self._generate_salt()
            self._data = None

    @property
    def data(self):
        if isinstance(self._data, str):
            return self._data.encode("UTF-8")
        elif self._data is not None:
            return bytes(self._data)
        else:
            return None

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def salt(self):
        if isinstance(self._salt, str):
            return self._salt.encode("UTF-8")
        elif self._salt is not None:
            return bytes(self._salt)
        else:
            return None

    @salt.setter
    def salt(self, value):
        self._salt = value

    @property
    def raw(self):
        if self.data is None:
            return None
        else:
            return bytes(self.salt) + bytes(self.data)

    @staticmethod
    def _transform_before_encrypt(data):
        return bytes(data)

    @staticmethod
    def _transform_after_decrypt(data):
        return bytes(data)

    @staticmethod
    def _generate_salt():
        return os.urandom(16)

    def _get_fernet_key(self, secret):
        secret = secret.encode("UTF-8") if isinstance(secret, str) else secret

        kdf = pbkdf2.PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=self.ITERATIONS,
            backend=backends.default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(secret))

        return key

    def encrypt(self, data, secret):
        if data is None:
            self.data = None

        else:
            key = self._get_fernet_key(secret)
            algo = fernet.Fernet(key)
            self.data = algo.encrypt(self._transform_before_encrypt(data))

        return self.data

    def decrypt(self, secret):
        if self.data is None:
            return None

        else:
            key = self._get_fernet_key(secret)
            algo = fernet.Fernet(key)

            return self._transform_after_decrypt(algo.decrypt(self.data))


class FernetTextFieldData(FernetBinaryFieldData):
    @staticmethod
    def _transform_before_encrypt(data):
        return data.encode("UTF-8")

    @staticmethod
    def _transform_after_decrypt(data):
        return data.decode("UTF-8")
