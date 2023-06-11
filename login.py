# import mysql.connector
# db = mysql.connector.connect(
#     host = "34.22.79.75",
#     user = "root",
#     password = "alex050601",
#     database = "mydb"
# )

class Login():
    def __init__(self):
        self.user_id = ""
        self.password = ""

    def login(self, user_id, password):
        self.user_id = user_id
        self.password = password
