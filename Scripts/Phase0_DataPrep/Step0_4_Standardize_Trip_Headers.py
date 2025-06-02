import os
import pandas as pd
import re

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
recommended_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Recommended_Header_Set.txt')
tripA_raw = os.path.join(base_path, 'Data', 'Raw_Data', 'TripA')
tripB_raw = os.path.join(base_path, 'Data', 'Raw_Data', 'TripB')
tripA_cleaned = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_Cleaned')
tripB_cleaned = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripB_Cleaned')

os.makedirs(tripA_cleaned, exist_ok=True)
os.makedirs(tripB_cleaned, exist_ok=True)

# === Load recommended headers
with open(recommended_path, 'r', encoding='utf-8') as f:
    recommended_headers = [line.strip() for line in f if line.strip() and "Recommended" not in line]

# === Fix map for known header issues
fix_map = {
    "Cabin Temperature Sensor [°C": "Cabin Temperature Sensor [°C]",
    "Temperature Vent right [°C": "Temperature Vent right [°C]",
    "max. SoC [%)": "max. SoC [%]",
    "Regenerative Braking Signal ": "Regenerative Braking Signal",
    "Velocity [km/h]]]": "Velocity [km/h]",
}

def clean_column(col):
    col = col.strip().strip(';')
    col = fix_map.get(col, col)
    col = re.sub(r'\]+$', ']', col)
    return col

def detect_separator(file_path):
    with open(file_path, 'r', encoding='ISO-8859-1') as f:
        line = f.readline()
        return ';' if line.count(';') > line.count(',') else ','

def standardize_file(in_path, out_path, rec_headers):
    try:
        sep = detect_separator(in_path)
        df = pd.read_csv(in_path, sep=sep, encoding='ISO-8859-1')
        df.columns = [clean_column(c) for c in df.columns]

        # Ensure all recommended headers are present
        for col in rec_headers:
            if col not in df.columns:
                df[col] = pd.NA

        # Reorder columns: Time [s] first
        ordered_cols = ['Time [s]'] + [col for col in rec_headers if col != 'Time [s]']
        df = df[ordered_cols]

        df.to_csv(out_path, index=False)
        print(f"✅ Cleaned with Time first: {os.path.basename(out_path)}")
    except Exception as e:
        print(f"❌ Error processing {os.path.basename(in_path)}: {e}")

def process_all(folder_in, folder_out, prefix, count):
    for i in range(1, count + 1):
        fname = f"{prefix}{str(i).zfill(2)}.csv"
        in_path = os.path.join(folder_in, fname)
        out_path = os.path.join(folder_out, fname.replace('.csv', '_cleaned.csv'))
        if os.path.exists(in_path):
            standardize_file(in_path, out_path, recommended_headers)
        else:
            print(f"⚠️ File missing: {fname}")

# === Process all files again with corrected order
process_all(tripA_raw, tripA_cleaned, "TripA", 32)
process_all(tripB_raw, tripB_cleaned, "TripB", 38)

print("\n✅ All files cleaned — Time [s] is now the first column.")
