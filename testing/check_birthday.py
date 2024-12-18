import pandas as pd
from datetime import datetime

def validate_birthdates(file_path, birthdate_column="Birthdate"):
    # Läs Excel-filen
    df = pd.read_excel(file_path)
    
    # Datum för dagens datum
    today = datetime.today()
    
    # Lista för ogiltiga datum
    invalid_dates = []

    # Kontrollera födelsedatumen
    for index, row in df.iterrows():
        try:
            birthdate = pd.to_datetime(row[birthdate_column], errors='coerce')
            if pd.isna(birthdate):
                invalid_dates.append((index, row[birthdate_column], "Datum är ogiltigt"))
            elif birthdate > today:
                invalid_dates.append((index, row[birthdate_column], "Datum i framtiden"))
            elif (today.year - birthdate.year) < 18 or (today.year - birthdate.year) > 100:
                invalid_dates.append((index, row[birthdate_column], "Ålder utanför tillåten gräns (18-100 år)"))
        except Exception as e:
            invalid_dates.append((index, row[birthdate_column], f"Fel: {str(e)}"))
    
    # Skriv ut resultat
    if invalid_dates:
        print("Ogiltiga födelsedatum hittades:")
        for idx, date, reason in invalid_dates:
            print(f"Rad {idx + 2}: {date} ({reason})")
    else:
        print("Alla födelsedatum är giltiga!")

# Exempelanvändning
file_path = "customer_data.xlsx"  # Ändra till din filväg
validate_birthdates(file_path)
