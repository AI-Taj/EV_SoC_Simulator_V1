import os
import pandas as pd

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
xls_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.xlsx')

# === Load CSV
df = pd.read_csv(csv_path)

# === Save as Excel
df.to_excel(xls_path, index=False)
print(f"✅ Saved as Excel:\n{xls_path}")
