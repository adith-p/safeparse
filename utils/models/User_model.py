class User_model:
    def __init__(self):
        self._user_authenticated = None
        self._user_id = None
        self._username = None

    def set_user_auth(self, flag: bool):
        self._user_authenticated = True

    def get_user_auth(self):
        return self._user_authenticated

    def set_user_id(self, id):
        self._user_id

    def get_user_id(self):
        return self._user_id

    def set_username(self, username):
        self._username = username

    def get_username(self):
        return self._username
