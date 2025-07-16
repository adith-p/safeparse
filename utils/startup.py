import apsw
from pathlib import Path


# def does_schema_exist(curr):
#     result: list = curr.execute(
#         """
#         SELECT tableName FROM sqlite_master WHERE type = 'table' AND name = 'users';
#         """
#     )
#     if not result:
#         return False
#     return True


# def init():


#     conn = apsw.Connection("vault.db")
#     curr = conn.cursor()
#     if not does_schema_exist(curr):
#         result = curr.execute(
#             """
#             CREATE TABLE users ()
#             """
#         )

DB_FILE = "vault.db"


def does_schema_exist(curr):
    """
    Checks if the 'users' table exists in the database.

    Args:
        curr: An apsw cursor object.

    Returns:
        bool: True if the 'users' table exists, False otherwise.
    """
    try:
        # Corrected SQL query: use 'name' column instead of 'tableName'
        result = curr.execute(
            """
            SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'users';
            """
        ).fetchone()  # Use fetchone() to get the first row or None
        return result is not None
    except apsw.Error as e:
        print(f"Error checking schema existence: {e}")
        return False


def init_db(encryption_key: str = None):
    """
    Initializes the database, creating necessary tables if they don't exist.
    This function will create the main 'users' table.
    Per-user vault tables will be created dynamically upon user registration/login.
    """
    conn = None  # Initialize conn to None for finally block
    try:
        # Connect to the database. If it doesn't exist, it will be created.
        conn = apsw.Connection(DB_FILE)
        curr = conn.cursor()
        curr.execute(f"PRAGMA key = '{encryption_key}';")
        # It's good practice to set cipher page size and KDF iterations for security
        curr.execute("PRAGMA cipher_page_size = 4096;")
        curr.execute("PRAGMA kdf_iter = 256000;")  # Recommended iterations for PBKDF2
        curr.execute("PRAGMA cipher_hmac_algorithm = HMAC_SHA512;")
        curr.execute("PRAGMA cipher_kdf_algorithm = PBKDF2_HMAC_SHA512;")
        print(f"Checking if database schema exists in {DB_FILE}...")
        if not does_schema_exist(curr):
            print("Schema does not exist. Creating 'users' table...")
            # Create the 'users' table with columns for user management
            # user_id: Primary key, unique identifier for each user
            # username: Unique username for login
            # master_password_hash: Stores the hashed master password
            # master_password_salt: Stores the salt used for hashing
            # (Consider adding a salt column for better security)
            curr.execute(
                """
                CREATE TABLE users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT NOT NULL UNIQUE,
                    master_password_hash TEXT NOT NULL,
                    master_password_salt TEXT NOT NULL
                );
                """
            )
            print("'users' table created successfully.")
            # TODO: Implement initial setup for per-user tables here if needed,
            # or ensure they are created dynamically when a user is first created.
            # For per-user tables, you'll likely create them when a new user registers.
            # Example: CREATE TABLE user_<user_id>_vault (...)
        else:
            print("Database schema already exists.")

    except apsw.Error as e:
        print(f"Database initialization error: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")
