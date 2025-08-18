from pathlib import Path
import gnupg


class EncryptionManager:
    def __init__(self, username: str, email: str) -> None:
        self.config_path: Path = Path("~/.safeparse/gpg").expanduser()
        self.username: str = username
        self.email: str = email
        self.key_type: str = "RSA"
        self.key_length = 4096
        self.gpg: gnupg.GPG

    def _create_config_folder(self):
        self.config_path.mkdir(parents=True, exist_ok=True)

    def init_encryption(self):
        self._create_config_folder()
        self.gpg = gnupg.GPG(gnupghome=str(self.config_path))
        self.gpg.encoding = "utf-8"
        return self

    def create_keys(self, password):
        key_input = self.gpg.gen_key_input(
            name_email=f"{self.username} <{self.email}>",
            passphrase=password,
            key_type=self.key_type,
            key_length=self.key_length,
        )
        self.gpg.gen_key(key_input)

    def get_all_keys(self):
        return self.gpg.list_keys()
