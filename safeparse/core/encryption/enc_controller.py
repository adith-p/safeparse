from enum import verify
import subprocess
from beaupy import confirm
from gnupg import Crypt
from .EncryptionManager import EncryptionManager
from safeparse.utils.menu_utils import (
    show_available_trust_level,
    show_enc_km_menu,
    show_enc_contacts_menu,
    show_key_menu,
    show_available_contacts,
    show_contact_fields,
    show_enc_edt_menu,
)
from rich import print
from safeparse.core.users.user_auth import user_request, verify_password
from safeparse.db.controllers import ContactDbController, UserDbController
from safeparse.core.vault.display_tables import display_tables_contact
from prompt_toolkit import prompt
from safeparse.core.encryption.encryption_handler import (
    decryption_handler,
    encryption_handler,
)
from getpass import getpass
from safeparse.logging.logger import logger

def key_extractor(key: list[dict]):
    key_id_list = []
    for items in key:
        key_id_list.append(f"{items["keyid"]} {items["uids"][0]}")

    return key_id_list


def key_management_handler(opt_number, enc: EncryptionManager):
    if opt_number == 0:
        # list all public keys
        key: list[dict] = enc.get_all_keys()
        key_list = key_extractor(key)
        key_selection = show_key_menu(key_list)
        try:
            key_to_get = key[key_selection]["keyid"]
            print(enc.gpg.export_keys(key_to_get))
        except TypeError:
            print("[red] select an option [/red]")
        logger.info("keyring viewed")
    if opt_number == 1:
        # add public key
        real_name = prompt("name> ")
        name_comment = prompt("name comment> ")
        email = prompt("email> ")
        passphrase =getpass("password> ")
        gpg_user_id = f"{real_name} <{email}>"

        enc.custom_create_keys(
            real_name=real_name,
            passphrase=passphrase,
            name_comment=name_comment,
            name_email=gpg_user_id,
        )
        logger.info("public key added")

    if opt_number == 2:
        # export public keys
        key: list[dict] = enc.get_all_keys()
        key_list = key_extractor(key)
        key_selection = show_key_menu(key_list)
        try:
            uid = key[key_selection]["uids"]
            user_email = uid[0].split()[-1]
            key_to_get = key[key_selection]["keyid"]
            public_key_path = str(enc.export_folder)
            with open(public_key_path + f"/{user_email}-public_key.enc", "w") as file:
                file.write(enc.gpg.export_keys(key_to_get))
            logger.info("public key exported")
        except TypeError:
            print("[red] select an option [/red]")

    if opt_number == 3:
        # import public key
        public_keys = [
            str(key).split("/")[-1]
            for key in enc.import_folder.iterdir()
            if key.is_file()
        ]
        key_selection = show_key_menu(public_keys)
        if key_selection != None:
            public_key_path = str(enc.import_folder) + f"/{public_keys[key_selection]}"
            public_key = enc.gpg.import_keys_file(public_key_path)

            if public_key.fingerprints[0]:
                contact_name = prompt("contact name> ")
                contact_email = prompt("contact email> ")
                ContactDbController().add_contact(
                    contact_name, contact_email, public_key.fingerprints[0]
                )
                print("[bold green] public key added to keyring [/bold green]")
                # Todo: Trusting the key
                print(public_key.fingerprints)

                # After import
                subprocess.run(
                    [
                        "gpg",
                        "--homedir",
                        str(enc.gpg.gnupghome),
                        "--lsign-key",
                        public_key.fingerprints[0],
                    ]
                )

        else:
            print(
                "[green]Please select [bold red]one file[/bold red] to import [/green]"
            )
    
    if opt_number == 4:
        all_keys = enc.get_all_keys()
        if not all_keys:
            print("No public key in the keyring")

        key_info_for_menu = key_extractor(all_keys)
        key_selection = show_key_menu(key_info_for_menu)
        selected_key = all_keys[key_selection]

        if not confirm(f"You are about to delete the key for {selected_key['uids'][0]}. Proceed?"):
            print("Deletion cancelled.")
            return
        db = UserDbController()
        user_primary_fingerprint = db.get_key_fingerprint(user_request["user_id"])

        if selected_key['fingerprint'] == user_primary_fingerprint[0]:
            print("[bold red]Error:[/bold red] You cannot delete the primary key associated with your account.")
            return

        password = getpass(f"Enter key password for {selected_key['uids'][0]} to confirm deletion> ").strip()
        if not password:
            print("Password cannot be empty. Deletion cancelled.")
            return

        master_hash_tuple = db.get_passhash(user_request["user_id"])
        if not master_hash_tuple:
            print("[bold red]Fatal Error:[/bold red] Could not retrieve user authentication hash from the database.")
            return

        if not verify_password(password, master_hash_tuple[0]):
            print("Incorrect password. Deletion cancelled.")
            return

        print(f"Attempting to delete key with fingerprint: {selected_key['fingerprint']}...")
        deletion_result = enc.delete_key(selected_key["fingerprint"],password)



    # TODO: opt_number is revoke this is a placeholder code for temp import
    if opt_number == 5:
        # revoke keys
        enc.revoke_key()



def update_contact_form(attribute: str) -> str:
    return prompt(f"{attribute}> ")


def convert_list(items: list[list[str]]) -> list:
    search_list = []
    for item in items:
        search_list.append(f"{item[1]}" + f"<{item[2]}>")
    return search_list


def convert_dict(items: list[str]) -> dict:
    update_field_dict = {}
    for item in items:
        db_key = item.replace(" ", "_")
        update_field_dict[db_key] = update_contact_form(item)
    return update_field_dict


def contacts_handler(opt_number: int):
    if opt_number == 0:
        """
        search for contacts
        """
        search_query = prompt("search> ")
        result = ContactDbController().get_contact(search_query)
        print(display_tables_contact(result))

    if opt_number == 1:
        """
        create contact
        """
        contact_name = prompt("contact name> ")
        contact_email = prompt("Email> ")
        fingerprint = prompt("public key fingerprint> ")
        ContactDbController().add_contact(
            contact_name=contact_name,
            contact_email=contact_email,
            fingerprint=fingerprint,
        )

    if opt_number == 2:
        "update contact"
        search_query = prompt("search> ")
        search_result = ContactDbController().get_contact(search_query)
        if search_result:
            contact_selection = show_available_contacts(convert_list(search_result))
            contact_fields = show_contact_fields()
            search_result = search_result[contact_selection]
            update_field_dict = convert_dict(contact_fields)
            ContactDbController().update_contacts(
                search_result[0], update_fields=update_field_dict
            )
            print("[bold green] contact details have been changed [/bold green]")
        else:
            print("[bold red] No results found [/bold red]")

    if opt_number == 3:
        """
        delete contact
        """
        search_query = prompt("search> ")
        search_result = ContactDbController().get_contact(search_query)
        if search_result:
            contact_selection = show_available_contacts(convert_list(search_result))
            search_result = search_result[contact_selection]
            ContactDbController().remove_contact(str(search_result[0]))
        else:
            print("[bold red] No results found [/bold red]")


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
    if selected_menu_option == 2:
        selected_sub_menu_option = show_enc_edt_menu()
        decryption_handler(selected_sub_menu_option, enc)
    if selected_menu_option == 3:
        selected_sub_menu_option = show_enc_contacts_menu()
        contacts_handler(selected_sub_menu_option)
