import os
import pyodbc
import sys

def check_db_connection():

    try:
        server = os.environ["AZURE_SQL_SERVER"]
        database = os.environ["AZURE_SQL_DATABASE"]
        user = os.environ["AZURE_SQL_USER"]
        password = os.environ["AZURE_SQL_PASSWORD"]

        connection_string = (
            f"Driver={{ODBC Driver 17 for SQL Server}};"
            f"Server={server};"
            f"Database={database};"
            f"Uid={user};"
            f"Pwd={password};"
        )

        conn = pyodbc.connect(connection_string, timeout=5)
        conn.close()

        print("Connection successful")
        sys.exit(0) 
    except Exception as e:
        print(f"Connection failed: {e}")
        sys.exit(1) 

if __name__ == "__main__":
    check_db_connection()