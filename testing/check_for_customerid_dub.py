import pandas as pd

def check_unique_customer_ids(file_path):
    # Läs in Excel-filen
    df = pd.read_excel(file_path)
    
    # Kontrollera att nödvändiga kolumner finns
    required_columns = ['CustomerID', 'First Name', 'Last Name', 'Birthdate']
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Filen saknar en eller flera kolumner: 'CustomerID', 'First Name', 'Last Name', 'Birthdate'.")

    # Kontrollera om CustomerID är unika
    if df['CustomerID'].is_unique:
        print("Alla CustomerID är unika!")
    else:
        print("Varning: Det finns dubbletter i CustomerID!")
        duplicates = df[df.duplicated(subset=['CustomerID'], keep=False)]
        print("Här är dubbletterna:\n", duplicates)

    # Kontrollera att samma kund (namn + födelsedatum) har samma ID
    grouped = df.groupby(['First Name', 'Last Name', 'Birthdate'])['CustomerID'].nunique()
    inconsistent = grouped[grouped > 1]

    if inconsistent.empty:
        print("Alla kunder har konsekventa CustomerID.")
    else:
        print("Varning: Följande kunder har flera CustomerID:")
        print(inconsistent)

# Använd funktionen
file_path = "customer_data_with_customer_id.xlsx"  # Din sparade fil
check_unique_customer_ids(file_path)