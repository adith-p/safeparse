import sqlite3
import uuid
from datetime import datetime

# import uuid
from sqlite3 import Connection
from typing import Any, Optional, Tuple

from safeparse.setting import VAULT_DB


class Db_controller:
    def __init__(self):
        self.db_name = VAULT_DB

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
            conn.close()


class UserDbController(Db_controller):

    def __init__(self):
        super().__init__()

    def create_user(
        self,
        user_id: str,
        username: str,
        email: str,
        hashed_password: bytes,
        hash_salt: bytes,
    ):
        query = "INSERT INTO users(user_id, username, email, master_password_hash, master_password_salt) VALUES (?, ?, ?,?, ?);"
        self._execute(
            query,
            (
                user_id,
                username,
                email,
                hashed_password,
                hash_salt,
            ),
            commit=True,
        )

    def get_user(self, user_id: str) -> Optional[Tuple]:
        query = "SELECT * FROM users WHERE user_id = ?;"
        return self._execute(query, (user_id,), fetchone=True)

    def get_user_by_username(self, username: str) -> Optional[Tuple]:
        query = "SELECT * FROM users WHERE username = ?;"
        return self._execute(query, (username,), fetchone=True)

    def get_passhash(self, user_id: str) -> Optional[Tuple]:
        query = "SELECT master_password_hash FROM users WHERE user_id = ?;"
        return self._execute(query, (user_id,), fetchone=True)

    def get_salt(self, user_id: str) -> Optional[Tuple]:
        query = "SELECT master_password_salt FROM users WHERE user_id = ?;"
        return self._execute(query, (user_id,), fetchone=True)

    def remove_user(self, user_id: str, password_hash: str) -> Optional[Tuple]:
        query = "DELETE FROM users WHERE user_id = ? and master_password_hash = ?;"
        return self._execute(
            query,
            (
                user_id,
                password_hash,
            ),
            commit=True,
        )


class PasswordDbController(Db_controller):

    def __init__(self):
        super().__init__()

    def get_passwords(self, current_user_id: str, search_params) -> list:

        query = """
                    SELECT password_id,login_username, password, notes, created_at, updated_at
                    FROM user_passwords
                    WHERE user_id = ? 
                        AND(
                          notes LIKE ?
                          OR login_username LIKE ?
                        ); \
                    """
        params = (current_user_id, f"%{search_params}%", f"%{search_params}%")
        return self._execute(query, params, fetchall=True)

    def set_password(
        self,
        current_user_id: str,
        note: str,
        login_password: str,
        login_username: str | None = None,
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

    def delete_password(self, password_id: str):
        query = "DELETE FROM user_passwords WHERE password_id = ?;"
        return self._execute(query, (password_id,), commit=True)

    def update_password(self, password_id: str, update_fields: dict):
        if not update_fields:
            return None

        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        query = f"UPDATE user_passwords SET {set_clause} WHERE password_id = ?;"

        values = list(update_fields.values()) + [password_id]

        return self._execute(query, tuple(values), commit=True)


class ContactDbController(Db_controller):
    def __init__(self):
        super().__init__()

    def add_contact(
        self,
        contact_name: str,
        contact_email: str,
        fingerprint: str,
    ):
        contact_id = str(uuid.uuid4())
        query = "INSERT INTO contacts(contact_id, contact_name, contact_email,key_fingerprint) VALUES (?, ?, ?, ?);"
        self._execute(
            query,
            (
                contact_id,
                contact_name,
                contact_email,
                fingerprint,
            ),
            commit=True,
        )

    def update_contacts(self, contact_id: str, update_fields: dict):
        if not update_fields:
            return None

        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        query = f"UPDATE contacts SET {set_clause} WHERE contact_id = ?;"

        values = list(update_fields.values()) + [contact_id]
        return self._execute(
            query,
            tuple(
                values,
            ),
            commit=True,
        )

    def get_all_contacts(self):
        query = "SELECT contact_name, contact_email, key_fingerprint FROM contacts;"
        return self._execute(query, fetchall=True)

    def get_contact(self, search_query: str) -> Optional[Any]:
        query = """
            SELECT
                contact_id,
                contact_name,
                contact_email,
                key_fingerprint
            FROM
                contacts
            WHERE
                contact_name LIKE (?) OR contact_email LIKE (?)
        """
        params = (f"%{search_query}%", f"%{search_query}%")
        return self._execute(
            query,
            params=params,
            fetchall=True,
        )

    def remove_contact(self, contact_id: str):
        query = "DELETE FROM contacts WHERE contact_id = (?)"
        return self._execute(query, (contact_id,), commit=True)
