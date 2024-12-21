import pandas as pd
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

df = pd.read_excel(input_file)
df.to_csv(output_file, index=False)
print(f"File converted to CSV: {output_file}")