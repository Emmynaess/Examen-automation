import os
import pandas as pd
import pyodbc

def upload_to_azure():
    file_path = "customer_data_valid/customer_data_deduped.xlsx"
    df = pd.read_excel(file_path)

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

    for index, row in df.iterrows():
        try:
          
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM Customer
                    WHERE FirstName = ? AND LastName = ? AND Birthdate = ?
                )
                BEGIN
                    INSERT INTO Customer (FirstName, LastName, Birthdate, CustomerCategory)
                    VALUES (?, ?, ?, ?)
                END
            """, row['First Name'], row['Last Name'], row['Birthdate'], row['First Name'], row['Last Name'], row['Birthdate'], row['Customer Category'])

         
            cursor.execute("""
                SELECT CustomerID FROM Customer
                WHERE FirstName = ? AND LastName = ? AND Birthdate = ?
            """, row['First Name'], row['Last Name'], row['Birthdate'])
            customer_id = cursor.fetchone()[0]

            
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM CustomerAddress
                    WHERE CustomerID = ? AND StreetName = ? AND Postalcode = ? AND City = ? AND Municipality = ?
                )
                BEGIN
                    INSERT INTO CustomerAddress (CustomerID, StreetName, Postalcode, City, Municipality)
                    VALUES (?, ?, ?, ?, ?)
                END
            """, customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'],
                customer_id, row['Streetname'], row['Postcode'], row['City'], row['Municipality'])

            
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM CustomerContactInformation
                    WHERE CustomerID = ? AND Phone = ? AND Email = ?
                )
                BEGIN
                    INSERT INTO CustomerContactInformation (CustomerID, Phone, Email)
                    VALUES (?, ?, ?)
                END
            """, customer_id, row['Phone'], row['Email'],
                customer_id, row['Phone'], row['Email'])

            
            cursor.execute("""
                IF NOT EXISTS (
                    SELECT 1 FROM Purchase
                    WHERE CustomerID = ? AND ProductID = ? AND PurchaseDate = ?
                )
                BEGIN
                    INSERT INTO Purchase (CustomerID, ProductID, PurchaseDate, Quantity, TotalAmount)
                    VALUES (?, ?, ?, ?, ?)
                END
            """, customer_id, row['ProductID'], row['Purchase Date'], customer_id, row['ProductID'], row['Purchase Date'], row['Quantity'], row['Total Amount'])

        except Exception as e:
            print(f"Fel på rad {index}: {e}")
            continue

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Data från {file_path} har laddats upp till SQL-databasen.")

if __name__ == "__main__":
    upload_to_azure()
