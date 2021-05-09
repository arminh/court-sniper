from configparser import ConfigParser

from cryptography.fernet import Fernet


class Config:

    config = None
    fernet = None
    tokenEndpoint = None
    sessionUrl = None
    courtsUrl = None
    clientId = None
    username = None
    password = None
    userId = None

    def __init__(self):
        key = Fernet.generate_key()        
        self.fernet = Fernet(key)

        self.config = ConfigParser()
        self.config.read('config.ini')

        self.tokenEndpoint = self.config.get('main', 'tokenEndpoint')
        self.courtsUrl = self.config.get('main', 'courtsUrl')
        self.clientId = self.config.get('main', 'clientId')
        self.sessionUrl = self.config.get("main", "sessionUrl")

        if self.config.has_option('main', 'username'):
            self.username = self.config.get('main', 'username')
        if self.config.has_option('main', 'password'):
            self.password = self.fernet.decrypt(self.config.get('main', 'password').encode()).decode()
        if self.config.has_option('main', 'userId'):
            self.userId = self.config.get('main', 'userId')

    def write_config_to_file(self, key: str, value: str):
        self.config.set("main", key, value)
        with open('config.ini', 'w') as f:
            self.config.write(f)

    def set_username(self, value: str):
        self.username = value;
        self.write_config_to_file("username", value)

    def set_password(self, value: str):
        self.password = value;
        self.write_config_to_file("password", self.fernet.encrypt(value.encode()).decode())

    def set_userId(self, value: str):
        self.userId = value;
        self.write_config_to_file("userId", value)

