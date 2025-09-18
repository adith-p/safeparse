from safeparse.db.controllers import PasswordDbController, UserDbController
from .psw_forms import get_psw_form, view_psw_form, update_psw_form
from prompt_toolkit import PromptSession
from rich import print
from safeparse.core.users.user_auth import password_hash
from safeparse.core.encryption.EncryptionManager import EncryptionManager
from safeparse.core.users.user_auth import user_request

def view_psw(password_entry: list):
    enc = EncryptionManager(user_request["username"],user_request["email"])
    enc.init_encryption()
    
    ciper_text = password_entry[2]
    if not ciper_text:
        print("password not found")
        return
    result = enc.decrypt_password(ciper_text)
    if result.ok:

        return result
    print(result.stderr)

def get_psw(current_usr_id: str) -> list:
    psw_tuple = view_psw_form()
    search_params = psw_tuple
    result = PasswordDbController().get_passwords(
        current_user_id=current_usr_id, search_params=search_params
    )
    return result


def put_paw(current_usr_id: str) -> list | None:
    enc = EncryptionManager(user_request["username"],user_request["email"])
    enc.init_encryption()
    psw_tuple = get_psw_form()

    if not psw_tuple:
        return
    username = psw_tuple[1]
    password = psw_tuple[0]
    notes = psw_tuple[2]

    user_fingerprint = UserDbController().get_key_fingerprint(user_request["user_id"])
    enc_result = enc.encrypt_password(user_fingerprint,password)
    if enc_result.ok:
        return PasswordDbController().set_password(
            current_user_id=current_usr_id,
            login_username=username,
            login_password=str(enc_result),
            note=notes,
        )
    print(f"[bold red]ERROR: [/bold red][bold green] {enc_result.stderr}")



def delete_paw(pass_id):

    PasswordDbController().delete_password(pass_id)
    print("Password [red]deleted[/Red]")


def update_password(password_id: str, custom_fields: list[int]):
    field_list = {}
    print(custom_fields)
    for field in custom_fields:
        field_list[field] = update_psw_form(field)

    PasswordDbController().update_password(password_id, field_list)
    print("[bold green]Password have been updated [/bold green]")
