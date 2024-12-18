import pandas as pd

def split_clean_and_dirty_data(input_file, clean_file, dirty_file):
    # Läs in Excel-filen
    df = pd.read_excel(input_file)

    # Definiera kriterier för felaktig data
    invalid_conditions = (
        df["First Name"].str.contains(r'\d', na=False) |  # Namn innehåller siffror
        ~df["Email"].str.contains("@", na=False) |        # Ogiltig email
        ~df["Phone"].str.startswith("+46", na=False) |    # Ogiltigt telefonnummer
        df["Streetname"].isin(["No Street"]) |            # Felaktiga adresser
        df["Postcode"].isin(["No Postcode"]) |
        df["City"].isin(["No City"]) |
        df["Municipality"].isin(["No Municipality"])
    )

    # Dela upp data i clean och dirty
    dirty_data = df[invalid_conditions]
    clean_data = df[~invalid_conditions]

    # Spara clean och dirty data till separata filer
    clean_data.to_excel(clean_file, index=False)
    dirty_data.to_excel(dirty_file, index=False)

    print(f"Clean data saved to '{clean_file}'")
    print(f"Dirty data saved to '{dirty_file}'")

if __name__ == "__main__":
    input_file = "customer_data.xlsx"
    clean_file = "clean_data.xlsx"
    dirty_file = "errors.xlsx"

    split_clean_and_dirty_data(input_file, clean_file, dirty_file)