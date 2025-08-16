from typing import Any

from prompt_toolkit import PromptSession


def get_psw_form() -> tuple[str, str, str]:
    session = PromptSession()
    password = session.prompt("password > ")
    username = session.prompt("username > ")
    note = session.prompt("Note > ")
    return (
        password,
        username,
        note,
    )


def view_psw_form() -> tuple[str, str]:
    session = PromptSession()
    search_params = session.prompt("search params >")

    return search_params
