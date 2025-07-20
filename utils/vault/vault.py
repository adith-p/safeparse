from pycparser.ply.yacc import resultlimit

from utils.database_controllers import PasswordDbController
from .psw_forms import get_psw_form, view_psw_form


def get_psw(current_usr_id: str) -> list:
    psw_tuple = view_psw_form()
    username = psw_tuple[0]
    notes = psw_tuple[1]
    result = PasswordDbController().get_passwords(
        current_user_id=current_usr_id,
        login_username=username,
        note=notes,
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
