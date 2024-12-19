from faker import Faker
import pandas as pd
import random

# Inställningar för svenska data
fake = Faker("sv_SE")

# Funktion för att generera svenska telefonnummer
def generate_swedish_phone_number():
    area_code = random.choice(["70", "72", "73", "76"])
    first_part = random.randint(100, 999)
    second_part = random.randint(10, 99)
    third_part = random.randint(10, 99)
    return f"+46 {area_code}-{first_part} {second_part} {third_part}"

# Funktion för att skapa testdata
def generate_test_customer_data(rows=20):
    domains = ["hotmail.com", "gmail.com", "outlook.com", "live.com", "icloud.com"]
    data = []

    for _ in range(rows):
        first_name = fake.first_name()
        last_name = fake.last_name()
        birthdate = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime('%Y-%m-%d')
        phone = generate_swedish_phone_number()
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"
        customer_category = random.choice(["Private", "Business"])
        street = fake.street_name()
        postcode = fake.postcode()
        city = fake.city()
        municipality = fake.state()

        # Generera flera köp för varje kund
        for _ in range(random.randint(1, 3)):  # Varje kund kan ha 1 till 3 köp
            purchase_date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
            product_id = random.randint(1000, 1010)  # Slumpmässigt ProductID för test
            quantity = random.randint(1, 5)
            price_per_item = random.uniform(50, 500)
            total_amount = round(price_per_item * quantity, 2)

            data.append({
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
                "ProductID": product_id,
                "Quantity": quantity,
                "Price per Item": round(price_per_item, 2),
                "Total Amount": total_amount
            })

    df = pd.DataFrame(data)
    return df

# Generera testdata
test_customer_data = generate_test_customer_data(20)

# Spara testdata till en Excel-fil
output_file = "customer_data.xlsx"
test_customer_data.to_excel(output_file, index=False)

print(f"Test data has been saved to {output_file}")
