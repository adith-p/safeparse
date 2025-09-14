from .EncryptionManager import EncryptionManager
from utils.menu_utils import (
    show_enc_km_menu,
    show_enc_contacts_menu,
    show_enc_edt_menu,
    show_key_menu,
    show_available_contacts,
    show_contact_fields,
)
from rich import print
from utils.users.user_auth import user_request
from utils.database_controllers import ContactDbController
from utils.vault.display_tables import display_tables_contact
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, Completer
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
        real_name = prompt("name> ")
        name_comment = prompt("name comment> ")
        email = prompt("email> ")
        passphrase = prompt("password> ")
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
        fingerprint = prompt("key fingerprint> ")
        enc.delete_key(fingerprint)

    # TODO: opt_number is revoke this is a placeholder code for temp import
    if opt_number == 4:
        public_key_path = str(enc.import_folder) + "/1.asc"
        enc.gpg.import_keys_file(public_key_path)


# encryption


# def encryption_handler(opt_number: int, enc: EncryptionManager):
#     contact_list = []
#     contacts = ContactDbController().get_all_contacts()
#     contact_list.append(ContactDbController().get_all_contacts())
#     contact_completer = WordCompleter(contact_list)
#     if opt_number == 0:
#         message_prompt = prompt("Message to encrypt> ")
#         contact_prompt = prompt("recipient> ", completer=contact_completer)
#         print(contact_prompt)
#

"""
def encryption_handler(opt_number: int, enc: EncryptionManager):
    
    Todo:

        -- accept the input through the session
        -- encrypt the session input to ciper text and txt file

        changelog:
            -- version 0.1.0
                --- Create a prototype for encryption
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
                                enc.gpg.trust_keys(key_fingerprint, "TRUST_FULLY")

                        else:
                            encrypted_text = str(encrypted_data)
                            print("Encryption successful!")
                            print("\nEncrypted Message (ASCII Armor):\n")
                            print(encrypted_text)
                else:
                    print(f"Key for {recipient_email} not found.")
"""


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
        db_key = item.replace(" ","_")
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
            ContactDbController().update_contacts(search_result[0], update_fields=update_field_dict)
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
    # if selected_menu_option == 1:
    #     selected_sub_menu_option = show_enc_edt_menu()
    #     encryption_handler(selected_sub_menu_option, enc)
    # if selected_menu_option == 2:
    #     pass
    if selected_menu_option == 3:
        selected_sub_menu_option = show_enc_contacts_menu()
        contacts_handler(selected_sub_menu_option)
