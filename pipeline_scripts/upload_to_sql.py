import os
import pandas as pd
import pyodbc

def upload_to_azure():
    # Uppdaterad sökväg till customer_data_deduped.xlsx
    file_path = "customer_data_valid/customer_data_deduped.xlsx"  # Korrekt sökväg
    df = pd.read_excel(file_path)

    # Hämta anslutningsinformation från miljövariabler
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

    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()

    # Ladda upp data
    for index, row in df.iterrows():
        # Lägg till i Customer-tabellen och få CustomerID
        cursor.execute("""
            INSERT INTO Customer (FirstName, LastName, Birthdate, CustomerCategory)
            OUTPUT INSERTED.CustomerID
            VALUES (?, ?, ?, ?)
        """, row['First Name'], row['Last Name'], row['Birthdate'], row['Customer Category'])
        customer_id = cursor.fetchone()[0]

        # Lägg till i CustomerAddress-tabellen
        cursor.execute("""
            INSERT INTO CustomerAddress (CustomerID, StreetName, Postalcode, City, Municipality)
            VALUES (?, ?, ?, ?, ?)
        """, customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'])

        # Lägg till i CustomerContactInformation-tabellen
        cursor.execute("""
            INSERT INTO CustomerContactInformation (CustomerID, Phone, Email)
            VALUES (?, ?, ?)
        """, customer_id, row['Phone'], row['Email'])

        # Kontrollera att ProductID existerar och lägg till i Purchase-tabellen
        cursor.execute("""
            SELECT COUNT(1) FROM Product WHERE ProductID = ?
        """, row['ProductID'])
        if cursor.fetchone()[0] > 0:
            cursor.execute("""
                INSERT INTO Purchase (CustomerID, ProductID, PurchaseDate, Quantity, TotalAmount)
                VALUES (?, ?, ?, ?, ?)
            """, customer_id, row['ProductID'], row['Purchase Date'], row['Quantity'], row['Total Amount'])
        else:
            print(f"Produkt med ProductID {row['ProductID']} saknas i Product-tabellen.")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data från {file_path} har laddats upp till SQL-databasen.")

if __name__ == "__main__":
    upload_to_azure()