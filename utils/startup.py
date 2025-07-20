import sqlite3
from pathlib import Path
import time
from typing import Callable
from prompt_toolkit.shortcuts import ProgressBar
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts.progress_bar import formatters

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
    except sqlite3.Error as e:
        print(f"Error checking schema existence: {e}")
        return False


def init_db():
    """
    Initializes the database, creating necessary tables if they don't exist.
    This function will create the main 'users' table.
    Per-user vault tables will be created dynamically upon user registration/login.
    """
    conn = None  # Initialize conn to None for finally block
    with ProgressBar(
        title=HTML("<b>Database Initialization</b>"),
        formatters=[
            formatters.Label(),
            formatters.SpinningWheel(),
            # formatters.Percentage(),
            # formatters.TimeElapsed(),
        ],
    ) as pb:
        progress_counter = pb(total=None, label="Initializing database")
        try:
            # Step 1:  Connect to the database. If it doesn't exist, it will be created.
            conn = sqlite3.connect(DB_FILE)
            curr = conn.cursor()
            # Step 2: Check schema (40%)
            progress_counter.label = "Checking database schema..."
            for i in range(20):
                time.sleep(0.0100)
                progress_counter.item_completed()

            schema_exist = does_schema_exist(curr)

            # print(f"Checking if database schema exists in {DB_FILE}...")
            if not schema_exist:
                # print("Schema does not exist. Creating 'users' table...")
                progress_counter.label = "Creating user tables..."
                for i in range(20):
                    time.sleep(0.0100)
                    progress_counter.item_completed()

                curr.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        user_id TEXT PRIMARY KEY,
                        username TEXT NOT NULL UNIQUE,
                        master_password_hash TEXT NOT NULL,
                        master_password_salt TEXT NOT NULL
                    );
                    """
                )
                conn.commit()
                for i in range(10):
                    time.sleep(0.0100)
                    progress_counter.item_completed()
                curr.execute(
                    """
                    CREATE TABLE IF NOT EXISTS user_passwords (
                    password_id TEXT PRIMARY KEY,
                    login_username TEXT,
                    notes TEXT,               
                    user_id TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE
                    );
                    """
                )
                curr.execute(
                    """
                    CREATE TRIGGER IF NOT EXISTS set_passwords_timestamp
                    AFTER UPDATE ON user_passwords
                    FOR EACH ROW
                    BEGIN
                        UPDATE passwords
                        SET updated_at = CURRENT_TIMESTAMP
                        WHERE id = OLD.id;
                    END;

                    """
                )
                conn.commit()
                print("'users' table created successfully.")
            else:
                progress_counter.label = "Schema already exists..."
                for i in range(20):
                    time.sleep(0.0100)
                    progress_counter.item_completed()
                print("Database schema already exists.")

            progress_counter.label = "Finalizing..."
            for i in range(60):
                time.sleep(0.0100)
                progress_counter.item_completed()

        except sqlite3.Error as e:
            print(f"Database initialization error: {e}")
        finally:
            if conn:
                conn.close()
                print("Database connection closed.")
