import pandas as pd
import os

def split_clean_and_dirty_data(input_file, clean_file, dirty_file):
    df = pd.read_excel(input_file)

    invalid_conditions = (
        df["First Name"].str.contains(r'\d', na=False) |  
        ~df["Email"].str.contains("@", na=False) |        
        ~df["Phone"].str.startswith("+46", na=False) |   
        df["Streetname"].isin(["No Street"]) |           
        df["Postcode"].isin(["No Postcode"]) |
        df["City"].isin(["No City"]) |
        df["Municipality"].isin(["No Municipality"])
    )

    dirty_data = df[invalid_conditions]
    clean_data = df[~invalid_conditions]

    os.makedirs("cleaned_data", exist_ok=True)
    os.makedirs("validate_data", exist_ok=True)

    clean_data.to_excel(f"cleaned_data/{clean_file}", index=False)
    dirty_data.to_excel(f"validate_data/{dirty_file}", index=False)

    print(f"Clean data saved to 'cleaned_data/{clean_file}'")
    print(f"Dirty data saved to 'validate_data/{dirty_file}'")

if __name__ == "__main__":
    input_file = "customer_data.xlsx"
    clean_file = "clean_data.xlsx"
    dirty_file = "errors.xlsx"

    if not os.path.exists(input_file):
        print(f'input file {input_file} does not exist')
        exit(1)

    split_clean_and_dirty_data(input_file, clean_file, dirty_file)