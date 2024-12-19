import pyodbc
import os

server = os.getenv("SQL_SERVER")
database = os.getenv("SQL_DATABASE")
username = os.getenv("SQL_USER")
password = os.getenv("SQL_PASSWORD")

try:
    conn = pyodbc.connect(
        f"Driver={{ODBC Driver 17 for SQL Server}};Server={server};Database={database};Uid={username};Pwd={password};Encrypt=yes;"
    )
    print("Database connection successful!")
    conn.close()
except Exception as e:
    print(f"Failed to connect to the database: {e}")
    exit(1)