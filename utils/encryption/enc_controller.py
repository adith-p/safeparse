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

def key_extractor(key: list[dict]):
    key_id_list = []
    for items in key:
        key_id_list.append(items["keyid"])

    return key_id_list


def key_management_handler(opt_number, enc:EncryptionManager):
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

"""
def decryption_handler(opt_number, enc: EncryptionManager):
    
    session = PromptSession()
    if opt_number == 0:
        cipher_text = session.prompt("enter the cipher text")
"""     

def render_sub_menus(selected_menu_option):
    enc = EncryptionManager(
        username=user_request["username"], email=user_request["email"]
    )
    enc.init_encryption()
    if selected_menu_option == 0:
        selected_sub_menu_option = show_enc_km_menu()
        key_management_handler(selected_sub_menu_option,enc)
