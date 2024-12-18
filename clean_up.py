import pandas as pd

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

    clean_data.to_excel(clean_file, index=False)
    dirty_data.to_excel(dirty_file, index=False)

    print(f"Clean data saved to '{clean_file}'")
    print(f"Dirty data saved to '{dirty_file}'")

if __name__ == "__main__":
    input_file = "customer_data.xlsx"
    clean_file = "clean_data.xlsx"
    dirty_file = "errors.xlsx"

    split_clean_and_dirty_data(input_file, clean_file, dirty_file)