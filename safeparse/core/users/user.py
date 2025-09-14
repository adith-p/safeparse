from safeparse.db.controllers import UserDbController
from safeparse.core.users.user_auth import get_current_user_id, password_hash, set_auth
from prompt_toolkit import PromptSession
from safeparse.logging.logger import logger


def user_command(parser):
    if parser.user_command == "delete":
        user_db = UserDbController()
        current_user_id = get_current_user_id()

        logger.info("Account deletion initiated for user_id: %s", current_user_id)
        session = PromptSession()
        password: str = session.prompt("password > ")
        if password.strip() == "":
            print("[red] Password cannot be empty [/red]")
            logger.warning(
                "Account deletion failed for user_id %s: Empty password submitted.",
                current_user_id,
            )
            return False

        if pass_salt := user_db.get_salt(current_user_id):
            psw_hash = password_hash(password, pass_salt[0])
            if psw_hash != user_db.get_passhash(current_user_id)[0]:
                print("[red] Password does not match [/red]")
                logger.warning(
                    "Account deletion failed for user_id %s: Incorrect password.",
                    current_user_id,
                )
                return False

            UserDbController().remove_user(
                user_id=current_user_id, password_hash=psw_hash
            )
            print("[green]User account deleted successfully[/green]")
            logger.info("Successfully deleted account for user_id: %s", current_user_id)
            set_auth(False)

        else:
            print("[red]Error: Could not verify user credentials.[/red]")
            logger.error(
                "Failed to retrieve salt or hash for user_id: %s. This indicates a potential database inconsistency.",
                current_user_id,
            )
            return False
    return True
