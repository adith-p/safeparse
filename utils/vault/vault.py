from utils.database_controllers import PasswordDbController
from .psw_forms import get_psw_form, view_psw_form
from prompt_toolkit import PromptSession
from rich import print
from ..users.user_auth import password_hash


def get_psw(current_usr_id: str) -> list:
    psw_tuple = view_psw_form()
    search_params = psw_tuple
    result = PasswordDbController().get_passwords(
        current_user_id=current_usr_id, search_params=search_params
    )
    return result


def put_paw(current_usr_id: str) -> list:
    psw_tuple = get_psw_form()
    username = psw_tuple[1]
    password = psw_tuple[0]
    notes = psw_tuple[2]

    result = PasswordDbController().set_password(
        current_user_id=current_usr_id,
        login_username=username,
        login_password=password,
        note=notes,
    )
    return result

def delete_paw():
    session = PromptSession()
    pass_id = session.prompt("Enter the password id > ")

    PasswordDbController().delete_password(pass_id)
    print("Password [red]deleted[/Red]")

