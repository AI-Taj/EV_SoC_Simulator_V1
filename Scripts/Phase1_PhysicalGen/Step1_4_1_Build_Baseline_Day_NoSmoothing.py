import numpy as np
import pandas as pd
import os
import random

# === Load paths ===
block_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_Baseline_NoSmoothing.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Load block library ===
block_data = np.load(block_file, allow_pickle=True)
block_library = {k: v.item() for k, v in block_data.items()}

# === Filter for driving, idle, regen
driving_blocks = [k for k, v in block_library.items() if v["segment_type"] == "driving"]
idle_blocks = [k for k, v in block_library.items() if v["segment_type"] == "idle"]
regen_blocks = [k for k, v in block_library.items() if v["segment_type"] == "regen"]

# === Generate Day Plan ===
random.seed(42)
day_plan = []

# Morning drive
day_plan += random.sample(driving_blocks, 3)
day_plan += random.sample(idle_blocks, 1)

# Afternoon drive
day_plan += random.sample(driving_blocks, 2)
if regen_blocks:
    day_plan += random.sample(regen_blocks, 1)
day_plan += random.sample(idle_blocks, 1)

# === Build synthetic day ===
time_offset = 0
rows = []

for block_id in day_plan:
    block = block_library[block_id]
    sig = block["signals"]
    n = len(sig["time"])

    for i in range(n):
        rows.append({
            "Time [s]": time_offset + i,
            "Current [A]": sig["current"][i],
            "Voltage [V]": sig["voltage"][i],
            "Temperature [°C]": sig["temperature"][i] if "temperature" in sig else np.nan,
            "SoC [%]": sig["soc_displayed"][i] if "soc_displayed" in sig else np.nan,
            "HVAC": block["hvac_on"],
            "SegmentType": block["segment_type"]
        })

    time_offset += n

# === Save to CSV ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"✅ Baseline day saved to:\n{output_csv}")
print(f"⏱️ Total duration: {df['Time [s]'].iloc[-1]} seconds")
print(f"📦 Segments used: {len(day_plan)}")
