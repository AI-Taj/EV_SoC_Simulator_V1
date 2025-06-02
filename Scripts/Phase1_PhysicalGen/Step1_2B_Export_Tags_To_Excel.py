import pandas as pd
import os

# === Paths ===
input_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.csv"
output_xlsx = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.xlsx"

# === Load CSV and save as Excel ===
df = pd.read_csv(input_csv)
df.to_excel(output_xlsx, index=False)

print(f"✅ Excel file saved to:\n{output_xlsx}")
