import pandas as pd
import sys

def validate_data(file_path):
    try:
        df = pd.read_excel(file_path)

        errors = []

        required_columns = [
            "First Name", "Last Name", "Birthdate", "Customer Category",
            "Streetname", "Postcode", "City", "Phone", "Email",
            "ProductID", "Purchase Date", "Quantity", "Total Amount"
        ]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            errors.append(f"Missing columns: {', '.join(missing_columns)}")

        for column in required_columns:
            if df[column].isnull().any():
                errors.append(f"Column '{column}' contains missing values.")

        if not pd.api.types.is_datetime64_any_dtype(df['Birthdate']):
            errors.append("Column 'Birthdate' must be a valid date.")
        if not pd.api.types.is_datetime64_any_dtype(df['Purchase Date']):
            errors.append("Column 'Purchase Date' must be a valid date.")
        if not pd.api.types.is_numeric_dtype(df['Quantity']):
            errors.append("Column 'Quantity' must be numeric.")
        if not pd.api.types.is_numeric_dtype(df['Total Amount']):
            errors.append("Column 'Total Amount' must be numeric.")

        if (df['Quantity'] < 0).any():
            errors.append("Column 'Quantity' contains negative values.")
        if (df['Total Amount'] < 0).any():
            errors.append("Column 'Total Amount' contains negative values.")

        invalid_emails = df[~df['Email'].str.contains(r'^[\w\.-]+@[\w\.-]+\.\w+$', na=False)]
        if not invalid_emails.empty:
            errors.append(f"Invalid email addresses found: {invalid_emails['Email'].tolist()}")

        invalid_phones = df[~df['Phone'].str.match(r'^\+46\s\d{2}-\d{3}\s\d{2}\s\d{2}$', na=False)]
        if not invalid_phones.empty:
            errors.append(f"Invalid phone numbers found: {invalid_phones['Phone'].tolist()}")

        if errors:
            print("Validation errors found:")
            for error in errors:
                print(f"- {error}")
            sys.exit(1) 
        else:
            print("Validation successful. No issues found.")

    except Exception as e:
        print(f"An error occurred during validation: {e}")
        sys.exit(1)  

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <file_path>")
        sys.exit(1)
    file_path = sys.argv[1]
    validate_data(file_path)