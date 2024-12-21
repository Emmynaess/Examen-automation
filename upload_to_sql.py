import pandas as pd
import pyodbc
import os
import sys

def upload_clean_data_to_sql(file_path, batch_size=100):
    
    server_name = os.getenv("SQL_SERVER")
    database_name = os.getenv("SQL_DATABASE")
    username = os.getenv("SQL_USER")
    password = os.getenv("SQL_PASSWORD")

    
    conn_str = (
        f"Driver={{ODBC Driver 17 for SQL Server}};"
        f"Server=tcp:{server_name};"
        f"Database={database_name};"
        f"Uid={username};"
        f"Pwd={password};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
        "Connection Timeout=30;"
    )

    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print("Database connection established.")

        
        df = pd.read_excel(file_path)

       
        customer_cache = set()

      
        for start_idx in range(0, len(df), batch_size):
            batch = df.iloc[start_idx:start_idx + batch_size]
            print(f"Processing batch {start_idx // batch_size + 1}...")

            for _, row in batch.iterrows():
                try:
               
                    customer_key = (row['First Name'], row['Last Name'], row['Birthdate'])

                    if customer_key not in customer_cache:
                        
                        cursor.execute("""
                            INSERT INTO Customer (FirstName, LastName, Birthdate, CustomerCategory)
                            VALUES (?, ?, ?, ?)
                        """, row['First Name'], row['Last Name'], row['Birthdate'], row['Customer Category'])

                        
                        cursor.execute("""
                            INSERT INTO CustomerAddress (StreetName, Postalcode, City, Municipality)
                            VALUES (?, ?, ?, ?)
                        """, row['Streetname'], row['Postcode'], row['City'], row['Municipality'])

                        
                        cursor.execute("""
                            INSERT INTO CustomerContactInformation (Phone, Email)
                            VALUES (?, ?)
                        """, row['Phone'], row['Email'])

                        
                        customer_cache.add(customer_key)

                    
                    cursor.execute("""
                        INSERT INTO Purchase (ProductID, PurchaseDate, Quantity, TotalAmount)
                        VALUES (?, ?, ?, ?)
                    """, row['ProductID'], row['Purchase Date'], row['Quantity'], row['Total Amount'])

                except Exception as row_error:
                    print(f"Error processing row: {row_error}")

            
            conn.commit()
            print(f"Batch {start_idx // batch_size + 1} committed.")

        print("All data successfully uploaded to the database.")

    except pyodbc.Error as db_error:
        print(f"Database connection error: {db_error}")
        sys.exit(1)
    except Exception as general_error:
        print(f"An unexpected error occurred: {general_error}")
        sys.exit(1)
    finally:
        if 'conn' in locals():
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Usage: python upload_to_sql.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    upload_clean_data_to_sql(file_path)
