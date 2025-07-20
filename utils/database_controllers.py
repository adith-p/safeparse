import sqlite3
import uuid
from datetime import datetime

# import uuid
from sqlite3 import Connection
from typing import Any, Optional, Tuple


class UserDbController:
    def __init__(self):
        self.db_name = "vault.db"

    def get_connection(self) -> Connection:
        return sqlite3.connect(self.db_name)

    def _execute(
            self, query: str, params: Tuple[Any, ...] = (), fetchone=False, commit=False
    ) -> Optional[Any]:
        conn = self.get_connection()
        curr = conn.cursor()
        try:
            curr.execute(query, params)
            if commit:
                conn.commit()
            if fetchone:
                return curr.fetchone()
            return curr
        except Exception as e:
            raise e
        finally:
            conn.close()

    def create_user(
            self, user_id: str, username: str, hashed_password: str, hash_salt: str
    ):
        query = "INSERT INTO users(user_id, username, master_password_hash, master_password_salt) VALUES (?, ?, ?, ?);"
        self._execute(
            query,
            (
                user_id,
                username,
                hashed_password,
                hash_salt,
            ),
            commit=True,
        )

    def get_user(self, username: str) -> Optional[Tuple]:
        query = "SELECT * FROM users WHERE username = ?;"
        return self._execute(query, (username,), fetchone=True)

    def get_passhash(self, username: str) -> Optional[Tuple]:
        query = "SELECT master_password_hash FROM users WHERE username = ?;"
        return self._execute(query, (username,), fetchone=True)

    def get_salt(self, username: str) -> Optional[Tuple]:
        query = "SELECT master_password_salt FROM users WHERE username = ?;"
        return self._execute(query, (username,), fetchone=True)

    def remove_user(self, username: str, password_hash: str) -> Optional[Tuple]:
        query = "DELETE FROM users WHERE username = ? and master_password_hash = ?;"
        return self._execute(
            query,
            (
                username,
                password_hash,
            ),
            commit=True,
        )


class PasswordDbController:
    def __init__(self):
        self.db_name = "vault.db"

    def get_connection(self) -> Connection:
        return sqlite3.connect(self.db_name)

    def _execute(
            self,
            query: str,
            params: Tuple[Any, ...] = (),
            fetchone: bool = False,
            fetchall: bool = False,
            commit: bool = False,
    ) -> Optional[Any]:
        conn = self.get_connection()
        curr = conn.cursor()

        try:
            curr.execute(query, params)

            if commit:
                conn.commit()
            if fetchone:
                return curr.fetchone()
            if fetchall:
                return curr.fetchall()

        except Exception as e:
            raise e
        finally:
            if conn:
                conn.close()

    def get_passwords(
            self, current_user_id: str, note: str, login_username: str = None
    ) -> list:

        if login_username:
            # Query with both note and username search from the correct table.
            query = """
                    SELECT login_username, password, notes, created_at, updated_at
                    FROM user_passwords
                    WHERE user_id = ?
                      AND notes LIKE ?
                      AND login_username LIKE ?; \
                    """
            params = (current_user_id, f"%{note}%", f"%{login_username}%")
        else:
            # Query with only note search.
            query = """
                    SELECT login_username, password, notes, created_at, updated_at
                    FROM user_passwords
                    WHERE user_id = ?
                      AND notes LIKE ?; \
                    """
            params = (current_user_id, f"%{note}%")

        return self._execute(query, params, fetchall=True)

    #
    def set_password(
            self,
            current_user_id: str,
            note: str,
            login_password: str,
            login_username: str = None,
    ) -> Any | None:
        password_id = str(uuid.uuid4())
        if login_username:

            query = """
                    INSERT INTO user_passwords(password_id, user_id, notes, password, login_username, created_at,
                                               updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?); \
                    """
            params = (
                password_id,
                current_user_id,
                note,
                login_password,
                login_username,
                datetime.now(),
                datetime.now(),
            )
        else:
            query = """
                    INSERT INTO user_passwords(password_id, user_id, notes, password, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?); \
                    """
            params = (
                password_id,
                current_user_id,
                note,
                login_password,
                datetime.now(),
                datetime.now(),
            )
        return self._execute(query, params, commit=True)
