import shlex

from rich import print
from prompt_toolkit import PromptSession

from utils.menu_utils import (
    get_password_config,
    show_main_menu,
    show_password_storage_menu,
    show_password_type_menu,
)

from utils.users.user_auth import auth_command, is_authenticated, get_current_user_id
from arg_parsers.parser import parent_parser

from utils.psw_utils import gen_password
from utils.users.user import user_command

from beaupy import ValidationError

from utils.vault import vault
from utils.vault.display_tables import display_tables

from utils.event_logging.logger import logger, print_log


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

        # Option 1: View/Save Passwords
        if opt == 1:
            current_user_id = get_current_user_id()
            storage_action = show_password_storage_menu()
            # View passwords
            if storage_action == 0:
                result = vault.get_psw(current_user_id)
                display_tables(result)
                logger.info(
                    "User (id: %s) is viewed passwords from the vault.", current_user_id
                )

            # Save password
            if storage_action == 1:
                vault.put_paw(current_user_id)
                logger.info("User (id: %s) saved an password", current_user_id)

            # Update passwords
            if storage_action == 2:
                pass

            # Delete Password
            if storage_action == 3:
                saved_passwords = vault.get_psw(current_user_id)
                display_tables(saved_passwords)
                vault.delete_paw()

        if opt == 2:
            # Option 2: viewing log
            print_log()

    return True
