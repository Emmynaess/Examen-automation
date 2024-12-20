# This code generates customer who buys more than one product

import pandas as pd
from faker import Faker
import random
import requests
import unicodedata
from datetime import datetime
import os
from config import AZURE_MAPS_API_KEY

fake = Faker("sv_SE")

# Counters for unique IDs
customer_id_counter = 1001
address_id_counter = 2001
contact_id_counter = 3001
purchase_id_counter = 4001

def load_products_from_csv(filename):
    try:
        filepath = os.path.join(os.path.dirname(__file__), filename)
        products_df = pd.read_csv(filepath)
        products_df["ProductID"] = range(3001, 3001 + len(products_df))
        return products_df.to_dict(orient="records")
    except Exception as e:
        print(f"Failed to load products from {filename}: {e}")
        return []

def generate_coordinates():
    lat = random.uniform(58.0, 63.0)
    lon = random.uniform(14.0, 20.0)
    return lat, lon

def get_address_from_coordinates(lat, lon, api_key):
    url = "https://atlas.microsoft.com/search/address/reverse/json"
    params = {
        'api-version': '1.0',
        'subscription-key': api_key,
        'query': f"{lat},{lon}",
        'language': 'sv-SE',
        'countrySet': 'SE'
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        addresses = data.get('addresses', [])
        if addresses:
            address_info = addresses[0].get('address', {})
            street = address_info.get('streetName', 'No Street')
            house_number = address_info.get('streetNumber', '')
            postcode = address_info.get('postalCode', 'No Postcode')
            city = address_info.get('municipalitySubdivision', 'No City')
            municipality = address_info.get('municipality', 'No Municipality')
            full_street = f"{street} {house_number}".strip()
            return full_street, postcode, city, municipality
    except requests.exceptions.RequestException as e:
        print(f"Error fetching address from coordinates: {e}")
    return "No Street", "No Postcode", "No City", "No Municipality"

def clean_string(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = s.replace(' ', '')
    return s

def generate_swedish_phone_number():
    area_code = random.choice(["70", "72", "73", "76"])
    first_part = random.randint(100, 999)
    second_part = random.randint(10, 99)
    third_part = random.randint(10, 99)
    return f"+46 {area_code}-{first_part} {second_part} {third_part}"

def generate_valid_purchase_date():
    today = datetime.today().date()
    return fake.date_between(start_date='-2y', end_date=today).strftime('%Y-%m-%d')

def generate_unique_ids():
    global customer_id_counter, address_id_counter, contact_id_counter, purchase_id_counter
    customer_id = int(customer_id_counter) 
    customer_id_counter += 1
    address_id = int(address_id_counter)
    address_id_counter += 1
    contact_id = int(contact_id_counter)
    contact_id_counter += 1
    return customer_id, address_id, contact_id

def generate_data(rows=10, max_retries=10):
    domains = ["hotmail.com", "gmail.com", "outlook.com", "live.com", "icloud.com"]
    products = load_products_from_csv("products.csv")

    data = []
    global purchase_id_counter

    for i in range(rows):
        # Assign IDs
        customer_id, address_id, contact_id = generate_unique_ids()
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
        phone = generate_swedish_phone_number()
        email = f"{clean_string(first_name)}.{clean_string(last_name)}@{random.choice(domains)}"
        customer_category = random.choice(["Private", "Business"])

        for attempt in range(max_retries):
            lat, lon = generate_coordinates()
            street, postcode, city, municipality = get_address_from_coordinates(lat, lon, AZURE_MAPS_API_KEY)
            if street != "No Street" and postcode != "No Postcode" and city != "No City" and municipality != "No Municipality":
                break
        else:
            street, postcode, city, municipality = "Fallback Street", "Fallback Postcode", "Fallback City", "Fallback Municipality"

        purchase_count = random.randint(1, 5)
        for _ in range(purchase_count):
            purchase_id = purchase_id_counter
            purchase_id_counter += 1

            purchase_date = generate_valid_purchase_date()
            product = random.choice(products)
            quantity = random.randint(1, 5)
            total_amount = product["price"] * quantity

            data.append({
                "CustomerID": customer_id,
                "AddressID": address_id,
                "ContactID": contact_id,
                "PurchaseID": purchase_id,
                "First Name": first_name,
                "Last Name": last_name,
                "Birthdate": birthdate,
                "Phone": phone,
                "Email": email,
                "Customer Category": customer_category,
                "Streetname": street,
                "Postcode": postcode,
                "City": city,
                "Municipality": municipality,
                "Purchase Date": purchase_date,
                "ProductID": product["productID"],
                "Product": product["productName"],
                "Quantity": quantity,
                "Price per Item": product["price"],
                "Total Amount": total_amount
            })

    df = pd.DataFrame(data)
    return df

def introduce_realistic_errors(df, error_probability=0.05):
    for idx in df.index:
        if random.random() < error_probability:
            error_type = random.choice([
                "typo_in_name", "invalid_email", "wrong_phone_format",
                "shifted_date", "missing_value", "duplicate_with_variation"
            ])

            if error_type == "typo_in_name":
                column = random.choice(["First Name", "Last Name"])
                name = df.at[idx, column]
                if len(name) > 3:
                    typo_index = random.randint(0, len(name)-2)
                    typo_name = name[:typo_index] + name[typo_index+1] + name[typo_index] + name[typo_index+2:]
                    df.at[idx, column] = typo_name

            elif error_type == "invalid_email":
                email = df.at[idx, "Email"]
                if "@" in email:
                    df.at[idx, "Email"] = email.replace("@", "")

            elif error_type == "wrong_phone_format":
                phone = df.at[idx, "Phone"]
                df.at[idx, "Phone"] = phone.replace(" ", "").replace("-", "") + random.choice(["", "0", "1"])

            elif error_type == "shifted_date":
                column = random.choice(["Birthdate", "Purchase Date"])
                date_value = df.at[idx, column]
                if date_value and "-" in date_value:
                    parts = date_value.split("-")
                    parts[0] = parts[0] + "2"
                    df.at[idx, column] = "-".join(parts)

            elif error_type == "missing_value":
                column = random.choice(["Email", "Phone"])
                df.at[idx, column] = ""

            elif error_type == "duplicate_with_variation":
                duplicate_row = df.loc[idx].copy()
                duplicate_row["Phone"] = generate_swedish_phone_number()
                df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)

    return df

def generate_and_corrupt_data(rows=10):
    df = generate_data(rows)
    df_with_errors = introduce_realistic_errors(df, error_probability=0.05)
    return df_with_errors

def save_to_excel(df, filename):
    df = df.sort_values(by="Purchase Date", ascending=False)
    df.to_excel(filename, index=False, float_format="%.0f")
    print(f"Excel file '{filename}' has been created.")

if __name__ == "__main__":
    customer_data = generate_and_corrupt_data(10)
    save_to_excel(customer_data, "customer_data.xlsx")
