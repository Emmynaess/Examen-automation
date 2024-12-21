import pandas as pd

def deduplicate_purchases(input_file: str, output_file: str) -> None:
    df = pd.read_excel(input_file)

    unique_key = ["FirstName", "LastName", "Email", "Phone", "PurchaseDate", "ProductID"]

    before = len(df)
    df = df.drop_duplicates(subset=unique_key, keep="first")
    after = len(df)

    print(f"Antal rader före dubblett-rensning: {before}")
    print(f"Antal rader efter dubblett-rensning: {after}")
    print(f"Antal borttagna dubblettrader: {before - after}")

    df.to_excel(output_file, index=False)
    print(f"Deduplicerad data sparad i: {output_file}")

if __name__ == "__main__":
    deduplicate_purchases(
        input_file="customer_data_valid.xlsx",
        output_file="customer_data_deduped.xlsx"
    )