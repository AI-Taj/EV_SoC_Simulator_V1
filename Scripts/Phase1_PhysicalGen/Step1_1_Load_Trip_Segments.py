import os
import pandas as pd
import numpy as np

# === Input Folders ===
trip_a_folder = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Processed_Trips\TripA_1s"
trip_b_folder = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Processed_Trips\TripB_1s"

# === Output File ===
output_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"
os.makedirs(os.path.dirname(output_file), exist_ok=True)

# === Required columns (update this list if needed) ===
required_columns = {
    "Time [s]": "time",
    "Battery Current [A]": "current",
    "Battery Voltage [V]": "voltage",
    "Battery Temperature [°C]": "temperature",
    "displayed SoC [%]": "soc_displayed",
    "Throttle [%]": "throttle",
    "Regenerative Braking Signal": "regen_signal",
    "Velocity [km/h]": "velocity",
    "AirCon Power [kW]": "aircon_power"
}

# === File loader ===
def load_trip_file(filepath):
    try:
        df = pd.read_csv(filepath)
        segment = {}
        for col, alias in required_columns.items():
            if col in df.columns:
                segment[alias] = df[col].to_numpy()
            else:
                print(f"⚠️ Column '{col}' missing in {os.path.basename(filepath)}")
                return None
        return segment
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None

# === Aggregate ===
all_segments = {}

def scan_folder(folder, prefix):
    for fname in sorted(os.listdir(folder)):
        if fname.endswith(".csv"):
            trip_name = os.path.splitext(fname)[0]
            full_id = f"{prefix}_{trip_name}"
            fpath = os.path.join(folder, fname)
            data = load_trip_file(fpath)
            if data:
                all_segments[full_id] = data
                print(f"✅ Loaded {full_id}")

# Load both TripA and TripB
scan_folder(trip_a_folder, "TripA")
scan_folder(trip_b_folder, "TripB")

# Save everything
np.savez_compressed(output_file, **all_segments)
print(f"\n🎉 All segments saved to:\n{output_file}")
