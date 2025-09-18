from os import path
from gnupg import Crypt
from prompt_toolkit import prompt
from .EncryptionManager import EncryptionManager
from safeparse.db.controllers import ContactDbController
from safeparse.utils.menu_utils import (
    show_available_contacts,
    show_file_to_encrypt_menu,
)
from rich import print
from pathlib import Path


def convert_list(items: list[list[str]]) -> list:
    search_list = []
    for item in items:
        search_list.append(f"{item[1]}" + f"<{item[2]}>")
    return search_list


def encryption_handler(opt_number: int, enc: EncryptionManager):
    # recipent is required for both cases.
    recipient = prompt("search> ")
    if recipient.strip() == "":
        print("recipent can't be empty")

    recipient_search_list = ContactDbController().get_contact(recipient)
    contact_selection = show_available_contacts(convert_list(recipient_search_list))
    fingerprint = recipient_search_list[contact_selection][3]

    if opt_number == 0:

        message_to_encrypt = prompt("message> ")
        if message_to_encrypt.strip() == "":
            print("Message can't be empty")

        # list keys
        if contact_selection == None:

            print("please select a recipent")
            return

        # encrypt messages
        encrypted_data: Crypt = enc.gpg.encrypt(
            message_to_encrypt, recipients=fingerprint
        )

        if not encrypted_data.ok:
            print("[bold red]Encryption failed[/bold red]")
            print(f"status: {encrypted_data.status}")
            print(f"Errors: {encrypted_data.stderr}")
        else:
            encrypted_text = str(encrypted_data)
            print("Encryption successful!")
            print("Encrypted Message: ")
            print(encrypted_text)

    if opt_number == 1:
        full_path = prompt("enter the path of file> ")
        if full_path.strip() == "":

            file_to_encrypt_list = [
                str(file).split("/")[-1]
                for file in enc.enc_folder.iterdir()
                if file.is_file()
            ]
            key_selection = show_file_to_encrypt_menu(file_to_encrypt_list)
            file_to_encrypt = file_to_encrypt_list[key_selection]
            # file_to_encrypt = str(enc.enc_folder) + f"/{str(file_to_encrypt)}"
            full_path = enc.enc_folder / file_to_encrypt
        full_path = Path(full_path)
        if not full_path.exists():
            print("[bold red] file to encrypt does not exists [/bold red]")
            return

        with full_path.open("rb") as f:
            result = enc.gpg.encrypt_file(
                f,
                recipients=fingerprint,
                sign=True,
                output=f"{full_path}.gpg",
            )

        print(f"decryption status: {result.status}")
        if not result.ok:
            print(f"decryption error: {result.stderr}")


def decryption_handler(opt_number: int, enc: EncryptionManager):
    if opt_number == 0:
        secret_message = prompt("message> ")
        message = enc.gpg.decrypt(message=secret_message)
        print(message)

    if opt_number == 1:
        full_path = prompt("enter the path of file> ")
        if full_path.strip() == "":

            file_to_encrypt_list = [
                str(file).split("/")[-1]
                for file in enc.dec_folder.iterdir()
                if file.is_file()
            ]
            key_selection = show_file_to_encrypt_menu(file_to_encrypt_list)
            file_to_encrypt = file_to_encrypt_list[key_selection]
            # file_to_encrypt = str(enc.dec_folder) + f"/{str(file_to_encrypt)}"
            full_path: Path = enc.dec_folder / file_to_encrypt
        full_path = Path(full_path)
        if not full_path.exists():
            print("[bold red] file to decrypt does not exists [/bold red]")
            return
        with full_path.open("rb") as f:
            result = enc.gpg.decrypt_file(
                f,
                output=str(full_path)
            )

        print(f"decryption status: {result.status}")
        if not result.ok:
            print(f"decryption error: {result.stderr}")
