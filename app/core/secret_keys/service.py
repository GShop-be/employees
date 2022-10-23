from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

from settings import Settings


class SecretKeys:
    def load_keys(self) -> None:
        try:
            with open(Settings.PRIVATE_KEY_PATH, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

                Settings.PRIVATE_KEY = private_key

            with open(Settings.PUBLIC_KEY_PATH, "rb") as key_file:
                public_key = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

                Settings.PUBLIC_KEY = public_key

        except FileNotFoundError:
            self.reinitialize()

    def reinitialize(self):
        self._initialize()
        self.load_keys()

    @staticmethod
    def _initialize():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        private_key_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        with open(Settings.PRIVATE_KEY_PATH, 'wb') as key_file:
            key_file.write(private_key_pem)

        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open(Settings.PUBLIC_KEY_PATH, 'wb') as key_file:
            key_file.write(pem)
