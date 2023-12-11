import sqlite3



class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                setfio TEXT,
                setbirthdate TEXT,
                setcontacts TEXT,
                setfaculty TEXT,
                setnickname TEXT,
                signup_status INTEGER DEFAULT 0
            )
        """)
        self.connection.commit()

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        self.connection.commit()

    def user_exists(self, user_id):
        self.cursor.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        return bool(result)

    def set_signup_status(self, user_id, status):
        self.cursor.execute("UPDATE users SET signup_status=? WHERE user_id=?", (status, user_id))
        self.connection.commit()

    def get_signup_status(self, user_id):
        self.cursor.execute("SELECT signup_status FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_fio(self, user_id, fio):
        self.cursor.execute("UPDATE users SET setfio=? WHERE user_id=?", (fio, user_id))
        self.connection.commit()

    def get_fio(self, user_id):
        self.cursor.execute("SELECT setfio FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_birthdate(self, user_id, birthdate):
        self.cursor.execute("UPDATE users SET setbirthdate=? WHERE user_id=?", (birthdate, user_id))
        self.connection.commit()

    def get_birthdate(self, user_id):
        self.cursor.execute("SELECT setbirthdate FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_contacts(self, user_id, contacts):
        self.cursor.execute("UPDATE users SET setcontacts=? WHERE user_id=?", (contacts, user_id))
        self.connection.commit()

    def get_contacts(self, user_id):
        self.cursor.execute("SELECT setcontacts FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_faculty(self, user_id, faculty):
        self.cursor.execute("UPDATE users SET setfaculty=? WHERE user_id=?", (faculty, user_id))
        self.connection.commit()

    def get_faculty(self, user_id):
        self.cursor.execute("SELECT setfaculty FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def set_nickname(self, user_id, nickname):
        self.cursor.execute("UPDATE users SET setnickname=? WHERE user_id=?", (nickname, user_id))
        self.connection.commit()

    def get_nickname(self, user_id):
        self.cursor.execute("SELECT setnickname FROM users WHERE user_id=?", (user_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None



