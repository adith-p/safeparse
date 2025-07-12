from .parent_parser import parent_parser


user_auth = parent_parser.add_subparsers(
    title="auth", description="command used for authenticating the user"
)
user_auth_parser = user_auth.add_parser(
    name="user",
    help="command to login a user",
)
user_auth_parser.add_argument("--username", required=True)
user_auth_parser.add_argument("--password", required=True)


# user_auth_parser.add_argument("--username", required=True)
# user_auth_parser.add_argument("--password", required=True)


user_creation_parser = user_auth.add_parser(
    name="create-user",
    help="command to create a new user",
)
user_creation_parser.add_argument("--username", required=True)
