import os
import pandas as pd

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Metadata_Filtered.csv')
xls_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Metadata_Filtered.xlsx')

# === Load CSV
df = pd.read_csv(csv_path)

# === Save as XLSX
df.to_excel(xls_path, index=False)
print(f"✅ Metadata exported to Excel at:\n{xls_path}")
