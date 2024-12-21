import os
import pyodbc
import sys
from server_and_database_name import server_name, database_name, database_password, database_username

def check_db_connection():
    """
    Försöker ansluta till en Azure SQL-databas med pyodbc.
    Hämtar inloggningsuppgifter från miljövariabler.
    Skriver ut 'Connection successful' om det lyckas,
    annars kastas ett undantag (och pipeline ska faila).
    """
    try:
        server = server_name
        database = database_name
        user = database_username
        password = database_password

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
