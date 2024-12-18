import pandas as pd
import pyodbc
from server_and_database_name import server_name, database_name, database_username, database_password

def upload_clean_data_to_sql(clean_data_file):
    
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server=tcp:{server_name};"
        f"Database={database_name};"
        f"Uid={database_username};"
        f"Pwd={database_password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

   
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

    df = pd.read_excel(clean_data_file)

   
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO Customer (FirstName, LastName, Birthdate, CustomerCategory)
            VALUES (?, ?, ?, ?)
        """, row['First Name'], row['Last Name'], row['Birthdate'], row['Customer Category'])

       
        cursor.execute("SELECT SCOPE_IDENTITY()")
        customer_id = cursor.fetchone()[0]

       
        cursor.execute("""
            INSERT INTO CustomerAddress (CustomerID, StreetName, Postalcode, City, Municipality)
            VALUES (?, ?, ?, ?, ?)
        """, customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'])

       
        cursor.execute("""
            INSERT INTO CustomerContactInformation (CustomerID, Phone, Email)
            VALUES (?, ?, ?)
        """, customer_id, row['Phone'], row['Email'])

       
        cursor.execute("""
            INSERT INTO Purchase (CustomerID, ProductID, PurchaseDate, Quantity, TotalAmount)
            VALUES (?, ?, ?, ?, ?)
        """, customer_id, row['ProductID'], row['Purchase Date'], row['Quantity'], row['Total Amount'])


    conn.commit()
    cursor.close()
    conn.close()
    print("Clean data successfully uploaded to Azure SQL!")

if __name__ == "__main__":
    clean_data_file = "clean_customer_data.xlsx"
    upload_clean_data_to_sql(clean_data_file)