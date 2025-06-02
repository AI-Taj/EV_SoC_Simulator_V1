import numpy as np

# === Adjust path as needed ===
npz_path = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"

# === Load the file ===
data = np.load(npz_path, allow_pickle=True)
all_keys = list(data.keys())
print(f"📁 Total trips loaded: {len(all_keys)}")

# Pick the first trip and inspect its keys
first_trip = data[all_keys[0]].item()
print(f"\n🔍 Sample trip ID: {all_keys[0]}")
print("📊 Available signals inside this trip:")
for k in first_trip.keys():
    print(f" - {k}")
