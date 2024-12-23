import pandas as pd

def deduplicate_purchases(input_file: str, output_file: str) -> None:
    df = pd.read_excel(input_file)

    print(f"Kolumner i DataFrame: {df.columns.tolist()}")

    unique_key = ["First Name", "Last Name", "Email", "Phone", "Purchase Date", "ProductID"]

    missing_columns = [col for col in unique_key if col not in df.columns]
    if missing_columns:
        raise KeyError(f"Följande kolumner saknas i DataFrame: {missing_columns}")

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
        input_file="customer_data_valid/customer_data_valid.xlsx",  
        output_file="customer_data_valid/customer_data_deduped.xlsx"  
    )