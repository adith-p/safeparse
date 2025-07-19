from simple_term_menu import TerminalMenu
from beaupy import confirm, prompt, select, select_multiple
from beaupy._internals import ValidationError


def menu_system():
    opts = ["generate password", "view/save passwords", "quit"]
    terminal_menu = TerminalMenu(opts)
    menu_entry = terminal_menu.show()
    # print(menu_entry)
    return menu_entry


def pass_menu():
    opts = ["default", "custom"]
    terminal_menu = TerminalMenu(opts)
    menu_entry = terminal_menu.show()
    return menu_entry


def pass_opt_menu():
    opts = [
        "use uppercase",
        "use lowercase",
        "use symbols",
        "use numbers",
    ]
    try:
        pass_len = prompt(
            "length of password", target_type=int, validator=lambda count: count > 5
        )
    except ValidationError as e:
        raise e

    return (
        select_multiple(opts, tick_character="*", ticked_indices=[], minimal_count=1),
        pass_len,
    )
