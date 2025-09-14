import secrets
import string
from rich import print


def gen_password(
    length=16,
    use_lower: bool = True,
    use_upper: bool = True,
    use_digit: bool = True,
    use_special: bool = True,
    custom_list: list | None = None,
):
    """
    Generate a secure random password based on selected character types.

    Parameters:
        length (int): Length of the password to generate. Default is 16.
        use_lower (bool): Include lowercase letters if True. Default is True.
        use_upper (bool): Include uppercase letters if True. Default is True.
        use_digit (bool): Include digits if True. Default is True.
        use_special (bool): Include special characters if True. Default is True.
        custom_list (list): Optional list to override default character types.
            Supported strings: "use uppercase", "use lowercase", "use numbers", "use symbols".
            If provided, only these character types will be used regardless of the boolean flags.

    Returns:
        str: A securely generated password string.

    Notes:
        - If no character sets are selected (either by booleans or custom_list), a message will be printed.
        - Uses the `secrets` module for cryptographic security.
    """

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
