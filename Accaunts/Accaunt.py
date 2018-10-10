class Account:
    def __init__(self):
        self.login = ""
        self._password = ""
        self.lvl = 0

    def get_lvl(self):
        return self.lvl
