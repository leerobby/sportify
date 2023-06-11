class Login():
    def __init__(self):
        self.user_id = ""
        self.password = ""
        self.count = 0

    def login(self, user_id, password):
        self.user_id = user_id
        self.password = password
