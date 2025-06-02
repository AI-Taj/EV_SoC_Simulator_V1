import os
import pandas as pd

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
tripA_cleaned = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_Cleaned')
tripB_cleaned = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripB_Cleaned')
tripA_downsampled = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_1s')
tripB_downsampled = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripB_1s')

os.makedirs(tripA_downsampled, exist_ok=True)
os.makedirs(tripB_downsampled, exist_ok=True)

# === Downsampling logic
def downsample_to_1s(file_path, save_path):
    try:
        df = pd.read_csv(file_path)
        if 'Time [s]' not in df.columns:
            raise ValueError("Missing 'Time [s]' column")

        # Round and group by 1-second bins
        df['Time [s]'] = df['Time [s]'].round(0).astype(int)
        df = df.sort_values('Time [s]')
        grouped = df.groupby('Time [s]', as_index=False)

        # Aggregate logic
        agg_funcs = {}
        for col in df.columns:
            if col == 'Time [s]':
                continue
            elif df[col].dtype == object:
                agg_funcs[col] = 'last'
            elif 'SoC' in col or 'State of Charge' in col:
                agg_funcs[col] = 'last'
            else:
                agg_funcs[col] = 'mean'

        df_downsampled = grouped.agg(agg_funcs)
        df_downsampled.to_csv(save_path, index=False)
        print(f"✅ Downsampled: {os.path.basename(save_path)}")
    except Exception as e:
        print(f"❌ Failed: {os.path.basename(file_path)} – {e}")

# === Process all files
def process_all(folder_in, folder_out, prefix, count):
    for i in range(1, count + 1):
        fname = f"{prefix}{str(i).zfill(2)}_cleaned.csv"
        in_path = os.path.join(folder_in, fname)
        out_path = os.path.join(folder_out, fname.replace("_cleaned.csv", "_d1s.csv"))
        if os.path.exists(in_path):
            downsample_to_1s(in_path, out_path)
        else:
            print(f"⚠️ Missing: {fname}")

# === Execute
process_all(tripA_cleaned, tripA_downsampled, "TripA", 32)
process_all(tripB_cleaned, tripB_downsampled, "TripB", 38)

print("\n✅ All files downsampled to 1-second resolution.")
