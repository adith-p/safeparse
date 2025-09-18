import shlex

from rich import print
from prompt_toolkit import PromptSession

from safeparse.core.encryption.enc_controller import render_sub_menus
from safeparse.utils.menu_utils import (
    get_password_config,
    show_enc_menu,
    show_main_menu,
    show_password_storage_menu,
    show_password_type_menu,
    update_password_menu,
    show_avail_passwords,
)

from safeparse.core.users.user_auth import (
    auth_command,
    is_authenticated,
    get_current_user_id,
)
from safeparse.cli.parser import parent_parser

from safeparse.utils.psw_utils import gen_password
from safeparse.core.users.user import user_command

from beaupy import ValidationError

from safeparse.core.vault import vault
from safeparse.core.vault.display_tables import display_tables,cipher_display_tables

from safeparse.logging.logger import logger, print_log


def menu_list(items):
    menu_entry = []
    for item in items:
        menu_entry.append(f"{item[0]} {item[1]}")
    return menu_entry

def dispatch(raw_string):
    session = PromptSession()
    tokens = shlex.split(raw_string)

    if not tokens:
        return None

    parser = parent_parser.parse_args(tokens)
    logger.info("Dispatching command: %s ", tokens[0])

    command = parser.command
    if command != "auth" and not is_authenticated():

        logger.warning("Blocked unauthenticated attempt to run command: '%s'", command)
        print("[red] You must be authenticated to run this command. [/red]")

        return None

    if command == "auth":
        auth_command(parser)

    if command == "user":
        # NOTE:- once the password vault have been set up work on this
        user_command(parser)

    if command == "menu":
        opt = show_main_menu()

        # Option 0: Generate Passwords
        if opt == 0:
            pass_type = show_password_type_menu()

            # Default Password
            if pass_type == 0:
                print(gen_password())
                logger.info("password generated.")

            # Custom Password
            elif pass_type == 1:
                try:
                    custom_options, pass_len = get_password_config()
                    print(gen_password(length=pass_len, custom_list=custom_options))
                    logger.info("password generated.")
                except ValidationError:
                    logger.warning(
                        "Custom password generation failed due to validation error: length less than 6."
                    )
                    print("[red]Password must be at least 6 characters long.")
                    return True

        # Option 1: Manage passwords
        if opt == 1:
            current_user_id = get_current_user_id()
            storage_action = show_password_storage_menu()
            # View passwords
            if storage_action == 0:
                saved_passwords = vault.get_psw(current_user_id)
                cipher_display_tables(saved_passwords)

                psw_list = menu_list(saved_passwords)
                selected_password = show_avail_passwords(psw_list)
                password_entry = saved_passwords[selected_password]
                result = vault.view_psw(password_entry)
                mutable_password_entry = list(password_entry)
                mutable_password_entry[2] = str(result) 
                print(mutable_password_entry)
                display_tables([mutable_password_entry])
                logger.info(
                    "User (id: %s) is viewed passwords from the vault.", current_user_id
                )

            # Save passwords
            if storage_action == 1:
                vault.put_paw(current_user_id)
                logger.info("User (id: %s) saved an password", current_user_id)

            # Update passwords
            if storage_action == 2:
                saved_passwords = vault.get_psw(current_user_id)
                if not saved_passwords:
                    print("vault is empty")
                    return
                display_tables(saved_passwords)
                psw_list = menu_list(saved_passwords)
                selected_password = show_avail_passwords(psw_list)
                psw_id = saved_passwords[selected_password][0]
                vault.update_password(psw_id, update_password_menu())

            # Delete Password
            if storage_action == 3:
                saved_passwords = vault.get_psw(current_user_id)
                if not saved_passwords:
                    print("vault is empty")
                display_tables(saved_passwords)
                psw_list = menu_list(saved_passwords)
                selected_password = show_avail_passwords(psw_list)
                psw_id = saved_passwords[selected_password][0]
                vault.delete_paw(psw_id)

        # Option 2: Printing the log files
        if opt == 2:
            print_log()

        # Option 3: encryption modules
        if opt == 3:
            enc_menu = show_enc_menu()
            render_sub_menus(enc_menu)
    return True
