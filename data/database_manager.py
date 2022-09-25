import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('db/blogs.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def checkUserId(self, id):
        requestUserId = f"SELECT id FROM users WHERE id = {id}"
        resultUserId = self.cursor.execute(requestUserId).fetchone()
        if resultUserId is not None:
            return True
        return False

    def checkUserInCoach(self, user_id, coach_id):
        requestAllUsers = f"SELECT users FROM coaches WHERE id = {coach_id}"
        resultAllUsers = list(self.cursor.execute(requestAllUsers).fetchone())
        if user_id not in resultAllUsers[0].split(';'):
            if self.addUserId(user_id=user_id, coach_id=coach_id, request_result=resultAllUsers):
                return True
            return False
        return False

    def addUserId(self, user_id, coach_id, request_result):
        finalId = f"{request_result[0]};{user_id}"
        requestAllUsers = f"UPDATE coaches SET users = '{finalId}' WHERE id = {coach_id}"
        print(requestAllUsers)
        self.cursor.execute(requestAllUsers)
        self.connection.commit()
        return True

    def getClients(self, id):
        requestClients = f"SELECT users FROM coaches WHERE id = {id}"
        resultClients = list(self.cursor.execute(requestClients).fetchone())[0].split(';')
        resultClients.pop(0)
        if len(resultClients) == 0:
            return "None"
        return resultClients
