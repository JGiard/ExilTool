class User:
    def __init__(self, username: str, crypted_password: str, active: bool, apikey: str):
        self.username = username
        self.crypted_password = crypted_password
        self.active = active
        self.apikey = apikey


class LoginRequest:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password


class Registration:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
