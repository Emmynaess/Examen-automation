import pandas as pd

def validate_data(file_path):
    df = pd.read_excel(file_path)

    null_values = df[df.isnull().any(axis=1)]

    invalid_email = df[~df['Email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)]

    invalid_phone = df[~df['Phone'].str.match(r'^\+46\d{9}$', na=False)]

    invalid_price = df[df['Total Price (kr)'] < 0]

    issues = pd.concat([null_values, invalid_email, invalid_phone, invalid_price]).drop_duplicates()

    issues.to_excel("validation_errors.xlsx", index=False)

if __name__ == "__main__":
    validate_data("customer_data.xlsx")
