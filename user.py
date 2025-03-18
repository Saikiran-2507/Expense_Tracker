from database import *

class User:
    def __init__(self, name, user_id, password):
        self.name = name
        self.user_id = user_id
        self.password = password
    
    @staticmethod
    def add_new_user(user):
        values = [user.name, user.user_id, user.password]
        conn, cur = db_connect()
        sel_qry = "SELECT User_id FROM Users"
        users = cur.execute(sel_qry).fetchall()
        users = [user[0] for user in users]
        while True:
            if user.user_id not in users:
                cur.execute("INSERT INTO Users VALUES(?, ?, ?)", values)
                break
            else:
                user.user_id = input("Try Another user id: ")
                values = [user.name, user.user_id, user.password]
        print("-----------------------------------------------------")
        print("            Account created successfully             ")
        print("-----------------------------------------------------")
        db_commit(conn)
        db_close(conn)

    @staticmethod
    def delete_user(user):
        if user != None:
            conn, cur = db_connect()
            if input("Do you really want to delete your account? (Yes or No)").lower() in ["yes", "y"]:
                cur.execute("DELETE FROM Transactions WHERE User_id = ?", (user.user_id,))
                cur.execute("DELETE FROM Users WHERE User_id = ?", (user.user_id,))
            db_commit(conn)
            db_close(conn)
            print("-----------------------------------------------------")
            print("        Your account is deleted successfully         ")
            print("-----------------------------------------------------")
        else:
            print("You are not logged in.\nYou need to login to your account to delete it.")
            return

    @staticmethod
    def update_user_password(user, value):
        if user != None:
            conn, cur = db_connect()
            cur.execute("UPDATE Users SET Password = ? WHERE User_id = ?", (value, user.user_id))
            db_commit(conn)
            db_close(conn)
            print("-----------------------------------------------------")
            print("           Password changed successfully             ")
            print("-----------------------------------------------------")
        else:
            print("You are not logged in.\nYou need to login to your account to password.")
            return

    
class Login_Manager():

    current_user = None
    
    @classmethod
    def login(cls, user_id, password):
        if cls.current_user == None:
            conn, cur = db_connect()
            sel_qry = "SELECT * FROM Users WHERE User_id = ?"
            usr = cur.execute(sel_qry, (user_id,)).fetchone()
            if usr == None:
                print("Invalid User_id")
                return 1
            else:
                if password == usr[2]:
                    cls.current_user = User(*usr)
                else:
                    print("Invalid Password")
                    return 2
            db_close(conn)
            print("-----------------------------------------------------")
            print(f"                 Welcome {cls.current_user.name}               ")
            print("-----------------------------------------------------")
            return 0
        else:
            print("Already Logged in. Logout first to login again.")
            return 3

    @classmethod
    def logout(cls):
        if cls.current_user != None:
            cls.current_user = None
            print("-----------------------------------------------------")
            print("              Successfully logged out                ")
            print("-----------------------------------------------------")
            return 0
        else:
            print("No account is logged in. Cannot logout.")
            return 1