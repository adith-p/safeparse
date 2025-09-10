from prompt_toolkit.shortcuts import print_container
from .EncryptionManager import EncryptionManager
from utils.menu_utils import (
    show_enc_km_menu,
    show_enc_contacts_menu,
    show_enc_edt_menu,
    show_key_menu,
)
from rich import print
from utils.users.user_auth import user_request
from prompt_toolkit import PromptSession

from gnupg import Crypt


def key_extractor(key: list[dict]):
    key_id_list = []
    for items in key:
        key_id_list.append(items["keyid"])

    return key_id_list


def key_management_handler(opt_number, enc: EncryptionManager):
    # list public key
    if opt_number == 0:
        key: list[dict] = enc.get_all_keys()
        key_list = key_extractor(key)
        key_selection = show_key_menu(key_list)
        try:
            key_to_get = key[key_selection]["keyid"]
            print(enc.gpg.export_keys(key_to_get))
        except TypeError:
            print("[red] select an option [/red]")

    if opt_number == 1:
        session = PromptSession()
        real_name = session.prompt("name> ")
        name_comment = session.prompt("name comment> ")
        email = session.prompt("email> ")
        passphrase = session.prompt("password> ")
        gpg_user_id = f"{real_name} <{email}>"

        enc.custom_create_keys(
            real_name=real_name,
            passphrase=passphrase,
            name_comment=name_comment,
            name_email=gpg_user_id,
        )

    if opt_number == 2:
        key: list[dict] = enc.get_all_keys()
        key_list = key_extractor(key)
        key_selection = show_key_menu(key_list)
        try:
            uid = key[key_selection]["uids"]
            user_email = uid[0].split()[-1]
            key_to_get = key[key_selection]["keyid"]
            public_key_path = str(enc.export_folder)
            with open(public_key_path + f"/{user_email}-public_key.txt", "w") as file:
                file.write(enc.gpg.export_keys(key_to_get))

        except TypeError:
            print("[red] select an option [/red]")

    if opt_number == 3:
        session = PromptSession()
        fingerprint = session.prompt("key fingerprint> ")
        enc.delete_key(fingerprint)

    if opt_number == 4:
        public_key_path = str(enc.import_folder) + "/1.asc"
        enc.gpg.import_keys_file(public_key_path)


# encryption


def encryption_handler(opt_number: int, enc: EncryptionManager):
    """
    Todo:

        -- accept the input through the session
        -- encrypt the session input to ciper text and txt file

        changelog:
            -- version 0.1.0
                --- Create a prototype for encryption
    """
    session = PromptSession()
    if opt_number == 0:
        plain_text = session.prompt("Message to encrypt> ")
        recipient_email = session.prompt("Enter the recipient email> ")

        all_keys = enc.gpg.list_keys()
        for key in all_keys:
            for uid in key["uids"]:
                print(uid)
                if recipient_email in uid:
                    print("in recipient email")
                    if key_fingerprint := key["fingerprint"]:
                        print(key)
                        encrypted_data: Crypt = enc.gpg.encrypt(
                            data=plain_text, recipients=key_fingerprint
                        )

                        if not encrypted_data.ok:
                            print("[bold red]Encryption failed[/bold red]")
                            print(f"status: {encrypted_data.status}")

                            trust = session.prompt("trust key> ")
                            if trust == "y":
                                enc.gpg.trust_keys(key_fingerprint, "TRUST_ULTIMATE")

                        else:
                            encrypted_text = str(encrypted_data)
                            print("Encryption successful!")
                            print("\nEncrypted Message (ASCII Armor):\n")
                            print(encrypted_text)
                else:
                    print(f"Key for {recipient_email} not found.")


def render_sub_menus(selected_menu_option):
    enc = EncryptionManager(
        username=user_request["username"], email=user_request["email"]
    )
    enc.init_encryption()
    if selected_menu_option == 0:
        selected_sub_menu_option = show_enc_km_menu()
        key_management_handler(selected_sub_menu_option, enc)
    if selected_menu_option == 1:
        selected_sub_menu_option = show_enc_edt_menu()
        encryption_handler(selected_sub_menu_option, enc)
