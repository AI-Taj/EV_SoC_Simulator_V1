import numpy as np
import pandas as pd
import os
import random

# === Load paths ===
block_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_SoC_Aligned.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Load block library ===
block_data = np.load(block_file, allow_pickle=True)
block_library = {k: v.item() for k, v in block_data.items()}

# === Segment selection ===
driving_blocks = [k for k, v in block_library.items() if v["segment_type"] == "driving"]
idle_blocks = [k for k, v in block_library.items() if v["segment_type"] == "idle"]
regen_blocks = [k for k, v in block_library.items() if v["segment_type"] == "regen"]

# === Build plan ===
random.seed(42)
day_plan = []
day_plan += random.sample(driving_blocks, 3)
day_plan += random.sample(idle_blocks, 1)
day_plan += random.sample(driving_blocks, 2)
if regen_blocks:
    day_plan += random.sample(regen_blocks, 1)
day_plan += random.sample(idle_blocks, 1)

# === Generate day with SoC alignment ===
time_offset = 0
rows = []
prev_soc_end = None

for block_id in day_plan:
    block = block_library[block_id]
    sig = block["signals"]
    n = len(sig["time"])

    # Extract SoC
    soc = sig["soc_displayed"]
    if soc is None or len(soc) < 2:
        print(f"⚠️ Skipping {block_id}, no usable SoC")
        continue

    # Align SoC if needed
    if prev_soc_end is not None:
        delta = prev_soc_end - soc[0]
        soc_aligned = soc + delta
    else:
        soc_aligned = soc

    prev_soc_end = soc_aligned[-1]

    for i in range(n):
        rows.append({
            "Time [s]": time_offset + i,
            "Current [A]": sig["current"][i],
            "Voltage [V]": sig["voltage"][i],
            "Temperature [°C]": sig["temperature"][i] if "temperature" in sig else np.nan,
            "SoC [%]": soc_aligned[i],
            "HVAC": block["hvac_on"],
            "SegmentType": block["segment_type"]
        })

    time_offset += n

# === Save output ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"✅ SoC-aligned day saved to:\n{output_csv}")
print(f"⏱️ Total duration: {df['Time [s]'].iloc[-1]} seconds")
print(f"📦 Segments used: {len(day_plan)}")
