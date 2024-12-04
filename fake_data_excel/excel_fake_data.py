import pandas as pd
from faker import Faker
import random
import requests
import numpy as np
from config import AZURE_MAPS_API_KEY
import time
import logging
import unicodedata
from datetime import datetime

fake = Faker("sv_SE")

logging.basicConfig(level=logging.INFO)

def generate_coordinates():
    lat_mean = 59.0  
    lat_std = 2.0    
    lon_mean = 15.0  
    lon_std = 2.0

    lat = np.random.normal(lat_mean, lat_std)
    lon = np.random.normal(lon_mean, lon_std)

    lat = np.clip(lat, 55.0, 69.0)
    lon = np.clip(lon, 11.0, 24.0)

    return lat, lon

def get_address_from_coordinates(lat, lon, api_key, max_retries=5):
    url = "https://atlas.microsoft.com/search/address/reverse/json"
    params = {
        'api-version': '1.0',
        'subscription-key': api_key,
        'query': f"{lat},{lon}",
        'language': 'sv-SE'
    }
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            addresses = data.get('addresses', [])
            if addresses:
                address_info = addresses[0].get('address', {})
                formatted_address = address_info.get('freeformAddress', '')
                postcode = address_info.get('postalCode', '')
                city = address_info.get('municipality', '')
                return formatted_address, postcode, city
            else:
                logging.warning(f"No address found for ({lat}, {lon}). Retrying...")
        except requests.exceptions.Timeout:
            logging.warning(f"Timeout during API call to Azure Maps for coordinates ({lat}, {lon}). Retrying...")
        except requests.exceptions.HTTPError as errh:
            logging.error(f"HTTP error: {errh}")
            break
        except requests.exceptions.ConnectionError as errc:
            logging.error(f"Connection error: {errc}")
            time.sleep(1)
        except requests.exceptions.RequestException as err:
            logging.error(f"Unknown error: {err}")
            break
        lat, lon = generate_coordinates()
        time.sleep(0.5)
    logging.error(f"Failed to retrieve address after {max_retries} attempts for coordinates ({lat}, {lon}).")
    return None, None, None

def clean_string(s):
    s = unicodedata.normalize('NFKD', s)
    s = s.encode('ascii', 'ignore').decode('ascii')
    s = s.lower()
    s = s.replace(' ', '')
    return s

def generate_swedish_phone_number():
    area_code = random.choice(["70", "72", "73", "76", "79"])
    first_part = random.randint(100, 999)
    second_part = random.randint(10, 99)
    third_part = random.randint(10, 99)
    return f"+46 {area_code}-{first_part} {second_part} {third_part}"

def generate_test_data(rows=100, error_chance=0.2):
    domains = ["hotmail.com", "gmail.com", "outlook.com", "live.com", "yahoo.com", "icloud.com"]

    data = {
        "CustomerID": list(range(1, rows + 1)),
        "First Name": [fake.first_name() for _ in range(rows)],
        "Last Name": [fake.last_name() for _ in range(rows)],
        "Birthdate": [
            fake.date_of_birth(minimum_age=18, maximum_age=90).strftime('%Y-%m-%d') for _ in range(rows)
        ],
        "Address": [],
        "Postcode": [],
        "City": [],
        "Phone": [generate_swedish_phone_number() for _ in range(rows)],
        "Customer Category": [random.choice(["Private", "Business"]) for _ in range(rows)],
        "Purchase Date": [
            fake.date_between(start_date='-3y', end_date='today').strftime('%Y-%m-%d') for _ in range(rows)
        ],
        "Purchase Amount (SEK)": [round(random.uniform(100, 10000), 2) for _ in range(rows)],
        "Purchase Count": [random.randint(1, 50) for _ in range(rows)],
    }

    emails = []
    for first, last in zip(data["First Name"], data["Last Name"]):
        first_email = clean_string(first)
        last_email = clean_string(last)
        domain = random.choice(domains)
        email = f"{first_email}.{last_email}@{domain}"
        emails.append(email)
    data["Email"] = emails

    for i in range(rows):
        for attempt in range(5):
            lat, lon = generate_coordinates()
            address, postcode, city = get_address_from_coordinates(lat, lon, AZURE_MAPS_API_KEY)
            if address and postcode and city:
                break
            else:
                logging.warning(f"Failed to retrieve address for customer {i+1}, attempt {attempt+1}")
        else:
            address = None
            postcode = None
            city = None
            logging.error(f"Could not retrieve address for customer {i+1} after 5 attempts.")

        data["Address"].append(address)
        data["Postcode"].append(postcode)
        data["City"].append(city)
        if (i + 1) % 10 == 0:
            logging.info(f"Processed {i+1}/{rows} customers")
        time.sleep(0.2) 

    df = pd.DataFrame(data)

    df[['Street', 'Rest']] = df['Address'].str.split(',', n=1, expand=True)

    df[['House Number', 'City From Address']] = df['Rest'].str.extract(r'(\d+)\s*(.*)')

    df = df.drop(columns=['Address', 'Rest'])

    df.dropna(subset=["Street", "Postcode", "City"], inplace=True)

    for idx in df.index:
        if random.random() < error_chance:
            if random.random() < 0.5:
                name_field = random.choice(["First Name", "Last Name"])
                name = df.loc[idx, name_field]
                name_with_errors = name
                if "ä" in name:
                    name_with_errors = name_with_errors.replace("ä", "a", 1)
                elif "å" in name:
                    name_with_errors = name_with_errors.replace("å", "a", 1)
                df.loc[idx, name_field] = name_with_errors

                first_email = clean_string(df.loc[idx, "First Name"])
                last_email = clean_string(df.loc[idx, "Last Name"])
                domain = random.choice(domains)
                df.loc[idx, "Email"] = f"{first_email}.{last_email}@{domain}"

            if random.random() < 0.3:
                col = random.choice(["First Name", "Last Name", "Phone", "Email", "Purchase Amount (SEK)"])
                df.loc[idx, col] = None

            if random.random() < 0.2:
                df.loc[idx, "Purchase Amount (SEK)"] = f"{df.loc[idx, 'Purchase Amount (SEK)']} kr"

            if random.random() < 0.2:
                df.loc[idx, "Purchase Amount (SEK)"] = random.uniform(-5000, -100)

    return df

def save_to_excel(df, filename):
    df.to_excel(filename, index=False)
    print(f"Excel file '{filename}' has been created.")

customer_data = generate_test_data(5, error_chance=0.2)
save_to_excel(customer_data, "customer_data.xlsx")
