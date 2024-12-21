import os
import pandas as pd

def format_phone_number(phone) -> str:
    # Hantera NaN och andra felaktiga format
    if pd.isna(phone):
        return ""  # Returnera en tom sträng för saknade värden
    if not isinstance(phone, str):
        phone = str(phone)  # Konvertera till sträng om det inte redan är en

    formatted_phone = phone.replace(" ", "")  # Ta bort mellanslag
    return formatted_phone

def main():
    df = pd.read_excel("customer_data.xlsx")

    # Formatera telefonnummer
    df["Phone"] = df["Phone"].apply(format_phone_number)

    # Definiera ogiltiga rader
    invalid_conditions = (
        df["First Name"].str.contains(r'\d', na=False) |
        ~df["Email"].str.contains("@", na=False) |
        ~df["Phone"].str.startswith("+46", na=False) |
        df["Streetname"].isin(["No Street"]) |
        df["Postcode"].isin(["No Postcode"]) |
        df["City"].isin(["No City"]) |
        df["Municipality"].isin(["No Municipality"])
    )

    df_invalid = df[invalid_conditions]
    df_valid = df[~invalid_conditions]

    # Skapa mappar för resultat
    os.makedirs("customer_data_valid", exist_ok=True)
    os.makedirs("customer_data_invalid", exist_ok=True)

    # Spara giltiga och ogiltiga rader
    df_valid.to_excel("customer_data_valid/customer_data_valid.xlsx", index=False)
    df_invalid.to_excel("customer_data_invalid/customer_data_invalid.xlsx", index=False)

    # Statistik och loggar
    print(f"Totalt antal rader: {len(df)}")
    print(f"Valid: {len(df_valid)} | Invalid: {len(df_invalid)}")
    print("Filer skapade:")
    print("  - customer_data_valid/customer_data_valid.xlsx")
    print("  - customer_data_invalid/customer_data_invalid.xlsx")

if __name__ == "__main__":
    main()












#---------------------

"""import os
import pandas as pd

def main():
    df = pd.read_excel("customer_data.xlsx")

    invalid_conditions = (
        df["First Name"].str.contains(r'\d', na=False)
        |
        ~df["Email"].str.contains("@", na=False)
        |
        ~df["Phone"].str.startswith("+46", na=False)
        |
        df["Streetname"].isin(["No Street"])
        |
        df["Postcode"].isin(["No Postcode"])
        |
        df["City"].isin(["No City"])
        |
        df["Municipality"].isin(["No Municipality"])
    )

    df_invalid = df[invalid_conditions]
    df_valid = df[~invalid_conditions]

    os.makedirs("customer_data_valid", exist_ok=True)
    os.makedirs("customer_data_invalid", exist_ok=True)

    df_valid.to_excel("customer_data_valid/customer_data_valid.xlsx", index=False)
    df_invalid.to_excel("customer_data_invalid/customer_data_invalid.xlsx", index=False)

    print(f"Totalt antal rader: {len(df)}")
    print(f"Valid: {len(df_valid)} | Invalid: {len(df_invalid)}")
    print("Filer skapade:")
    print("  - customer_data_valid/customer_data_valid.xlsx")
    print("  - customer_data_invalid/customer_data_invalid.xlsx")

if __name__ == "__main__":
    main()"""