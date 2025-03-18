import datetime
from database import *
from tabulate import tabulate
import user

class Transaction():
    def __init__(self, date, type, amount, category, description):
        self.date = Transaction.validate_date(date)
        self.type = Transaction.validate_type(type)
        self.amount = Transaction.validate_amount(amount)
        self.category = category
        self.description = description

    def __str__(self):
        return f"""Date: {self.date}
Transaction_Type: {self.type}
Amount: {self.amount}
Category: {self.category}
Description: {self.description}"""

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = Transaction.validate_amount(amount)

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, type):
        self._type = Transaction.validate_type(type)

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = Transaction.validate_date(date)

    @staticmethod
    def validate_date(date):
        try:
            values = list(map(int, date.split("-")))
            datetime.date(*values)
            return date
        except ValueError:
            raise ValueError("****Invalid Date****")
    
    @staticmethod
    def validate_type(type):
        try:
            if type.lower() not in ["income", "expense"]:
                raise ValueError
            return type
        except ValueError:
            raise ValueError("****Invalid Type****")
    
    @staticmethod
    def validate_amount(amount):
        try:
            amount = float(amount)
            if amount < 0:
                raise ValueError
            return amount
        except ValueError:
            raise ValueError("****Invalid Amount****")
    

class Transaction_Manager():

    def add_transaction(trans, user):
        conn, cur = db_connect()
        cur.execute("INSERT INTO Transactions VALUES(?, ?, ?, ?, ?, ?)", ( user.user_id, trans.date, trans.type, trans.amount, trans.category, trans.description))
        print("-----------------------------------------------------")
        print("           Transaction added successfully            ")
        print("-----------------------------------------------------")
        db_commit(conn)
        db_close(conn)

    def view_transactions(user):
        conn, cur = db_connect()
        transactions = cur.execute("SELECT  Transaction_id, Date, Type, Amount, Category, Description FROM Transactions WHERE User_id = ?", (user.user_id,)).fetchall()
        db_commit(conn)
        db_close(conn)
        if len(transactions) != 0:
            headers = ["Transaction_id", "Date", "Type", "Amount", "Category", "Description"]
            print(tabulate(transactions, headers, tablefmt="grid"))
            print()
            return 1
        else:
            print("-----------------------------------------------------")
            print("                  No Transactions                    ")
            print("-----------------------------------------------------")
            return 0

    def edit_transaction(transaction_id, edit_attr, value):
        conn, cur = db_connect()
        query = f"UPDATE Transactions SET {edit_attr} = ? WHERE Transaction_id = ?"
        cur.execute(query, (value, transaction_id))
        db_commit(conn)
        db_close(conn)
        print("-----------------------------------------------------")
        print("            Transaction edited successfully          ")
        print("-----------------------------------------------------")
        return


    def delete_transaction(transaction_id):
        conn, cur = db_connect()
        cur.execute("DELETE FROM Transactions WHERE Transaction_id = ?", (transaction_id,))
        db_commit(conn)
        db_close(conn)
        print("-----------------------------------------------------")
        print("           Transaction deleted successfully          ")
        print("-----------------------------------------------------")
        return

    def get_transaction_object(transaction_id):
        conn, cur = db_connect()
        t = cur.execute("SELECT Date, Type, Amount, Category, Description FROM Transactions WHERE Transaction_id = ?", (transaction_id,)).fetchone()
        db_commit(conn)
        db_close(conn)
        return Transaction(*t)