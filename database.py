import pyodbc
import sys

def db_connect():
    try:
        driver = 'SQL SERVER'
        server = 'DESKTOP-EIV7VDA\\SQLEXPRESS'
        database = 'FinanceTracker'

        Connection_string = f"""
            DRIVER={{{driver}}}
            SERVER={server};
            DATABASE={database};
            Trusted_Connection=yes;
        """
        conn = pyodbc.connect(Connection_string)
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(e)
        sys.exit()

def db_commit(connection):
    try:
        connection.commit()
    except Exception as e:
        print(e)
        sys.exit()

def db_close(connection):
    try: 
        connection.close()  
    except Exception as e:
        print(e)
        sys.exit()