from safeparse.db.controllers import PasswordDbController
from .psw_forms import get_psw_form, view_psw_form, update_psw_form
from prompt_toolkit import PromptSession
from rich import print
from safeparse.core.users.user_auth import password_hash


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


def update_password(password_id: str, custom_fields: list[int]):
    field_list = {}
    print(custom_fields)
    for field in custom_fields:
        field_list[field] = update_psw_form(field)

    PasswordDbController().update_password(password_id, field_list)
    print("[bold green]Password have been updated [/bold green]")
