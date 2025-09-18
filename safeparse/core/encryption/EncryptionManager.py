from pathlib import Path
import gnupg


class EncryptionManager:
    def __init__(self, username: str, email: str) -> None:
        self.config_path: Path = Path("~/.safeparse/gpg").expanduser()
        self.export_folder: Path = Path("~/.safeparse/gpg/export_keys").expanduser()
        self.import_folder: Path = Path("~/.safeparse/gpg/import_keys").expanduser()
        self.enc_folder: Path = Path("~/.safeparse/enc_folder").expanduser()
        self.dec_folder: Path = Path("~/.safeparse/dec_folder").expanduser()
        self.username: str = username
        self.email: str = email
        self.key_type: str = "RSA"
        self.key_length = 4096
        self.gpg: gnupg.GPG

    def _create_config_folder(self):
        self.config_path.mkdir(parents=True, exist_ok=True)
        self.export_folder.mkdir(parents=True, exist_ok=True)
        self.import_folder.mkdir(parents=True, exist_ok=True)
        self.enc_folder.mkdir(parents=True, exist_ok=True)
        self.dec_folder.mkdir(parents=True, exist_ok=True)

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
            name_real=self.username,
        )
        return self.gpg.gen_key(key_input)

    def get_all_keys(self):
        return self.gpg.list_keys()

    def custom_create_keys(
        self,
        real_name: str,
        passphrase: str,
        name_comment: str,
        name_email: str,
        key_type: str = "RSA",
        key_length: str = "4096",
    ):
        key_input = self.gpg.gen_key_input(
            name_email=name_email,
            key_type=key_type,
            key_length=key_length,
            name_real=real_name,
            name_comment=name_comment,
            passphrase=passphrase,
        )
        self.gpg.gen_key(key_input)

    def revoke_key(self):
        enc = self.gpg

    def delete_key(self, fingerprint):
        self.delete_key(fingerprint)
        print("[bold green] Key deleted [/bold green]")
