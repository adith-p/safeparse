import secrets
import string
from rich import print


def gen_password(
    length=16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digit: bool = True,
    use_special: bool = True,
    custom_list: list = None,
):
    opts = [
        "use uppercase",
        "use lowercase",
        "use symbols",
        "use numbers",
    ]

    if custom_list:

        if "use uppercase" not in custom_list:
            use_upper = False
        if "use lowercase" not in custom_list:
            use_lower = False
        if "use symbols" not in custom_list:
            use_special = False
        if "use numbers" not in custom_list:
            use_digit = False

    pool = ""
    if use_lower:
        pool += string.ascii_lowercase
    if use_upper:
        pool += string.ascii_uppercase
    if use_digit:
        pool += string.digits
    if use_special:
        pool += string.punctuation

    if not pool:
        print("[red] At least one character set must be selected [/red]")

    password = "".join(secrets.choice(pool) for _ in range(length))

    return password
