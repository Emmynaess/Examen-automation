import pandas as pd

def main():
    df = pd.read_excel("customer_data.xlsx")

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

    df_valid.to_excel("customer_data_valid.xlsx", index=False)
    df_invalid.to_excel("customer_data_invalid.xlsx", index=False)

    print("=================================")
    print(f"Antal rader valid: {len(df_valid)}")
    print(f"Antal rader invalid: {len(df_invalid)}")
    print("Filer skapade:")
    print(" - customer_data_valid.xlsx")
    print(" - customer_data_invalid.xlsx")
    print("=================================")

if __name__ == "__main__":
    main()