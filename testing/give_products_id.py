import pandas as pd

excel_file = "customer_data.xlsx"  
output_file = "customer_data_product_ids.xlsx"
df = pd.read_excel(excel_file)

products_df = pd.read_csv("products_with_id.csv")

product_mapping = products_df.set_index("ProductName")["ProductID"].to_dict()

df['ProductID'] = df['Product'].apply(lambda x: product_mapping.get(x, None)).astype('Int64')

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    df.to_excel(writer, index=False, sheet_name="Sheet1")
    worksheet = writer.sheets['Sheet1']
    for col in worksheet.iter_cols(min_col=worksheet.max_column, max_col=worksheet.max_column):
        for cell in col:
            cell.number_format = '0'

print(f"Uppdaterad fil sparad som '{output_file}' med ProductID utan komma.")