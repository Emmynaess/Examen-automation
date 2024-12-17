import pandas as pd
import os

def generate_unique_customer_ids(input_file, output_file):
    df = pd.read_excel(input_file)

    required_columns = ["First Name", "Last Name", "Birthdate"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Kolumnen '{col}' saknas i filen!")

    df['Unique Key'] = df['First Name'] + df['Last Name'] + df['Birthdate']

    unique_keys = df['Unique Key'].unique()
    unique_id_mapping = {key: idx for idx, key in enumerate(unique_keys, start=1001)}

    df['Customer ID'] = df['Unique Key'].map(unique_id_mapping)

    df.drop(columns=['Unique Key'], inplace=True)

    df.to_excel(output_file, index=False)
    print(f"Uppdaterad Excel-fil sparad som: {output_file}")

if __name__ == "__main__":
    input_file = "customer_data.xlsx"
    output_file = "customer_data_with_ids.xlsx"
    generate_unique_customer_ids(input_file, output_file)

