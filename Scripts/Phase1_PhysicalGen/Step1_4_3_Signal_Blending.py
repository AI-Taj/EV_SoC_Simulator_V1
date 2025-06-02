import numpy as np
import pandas as pd
import os
import random

# === Config ===
BLEND_WINDOW = 5  # seconds

# === Paths ===
block_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_Blended_Current_Voltage.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Load data ===
block_data = np.load(block_file, allow_pickle=True)
block_library = {k: v.item() for k, v in block_data.items()}

driving_blocks = [k for k, v in block_library.items() if v["segment_type"] == "driving"]
idle_blocks = [k for k, v in block_library.items() if v["segment_type"] == "idle"]
regen_blocks = [k for k, v in block_library.items() if v["segment_type"] == "regen"]

# === Build day plan ===
random.seed(42)
day_plan = []
day_plan += random.sample(driving_blocks, 3)
day_plan += random.sample(idle_blocks, 1)
day_plan += random.sample(driving_blocks, 2)
if regen_blocks:
    day_plan += random.sample(regen_blocks, 1)
day_plan += random.sample(idle_blocks, 1)

# === Build day with current/voltage blending ===
time_offset = 0
rows = []
prev_block = None

for block_id in day_plan:
    block = block_library[block_id]
    sig = block["signals"]
    n = len(sig["time"])

    soc = sig["soc_displayed"]
    if soc is None or len(soc) < 2:
        print(f"⚠️ Skipping {block_id} (missing SoC)")
        continue

    current = sig["current"]
    voltage = sig["voltage"]

    # Prepare signals with optional blending
    for i in range(n):
        blend_factor = 1.0  # default

        if prev_block and i < BLEND_WINDOW:
            # Linear blend: from prev_block to current block
            alpha = (BLEND_WINDOW - i) / BLEND_WINDOW
            current_prev = prev_block["signals"]["current"][-BLEND_WINDOW + i]
            voltage_prev = prev_block["signals"]["voltage"][-BLEND_WINDOW + i]

            current_blend = alpha * current_prev + (1 - alpha) * current[i]
            voltage_blend = alpha * voltage_prev + (1 - alpha) * voltage[i]
        else:
            current_blend = current[i]
            voltage_blend = voltage[i]

        rows.append({
            "Time [s]": time_offset + i,
            "Current [A]": current_blend,
            "Voltage [V]": voltage_blend,
            "Temperature [°C]": sig["temperature"][i] if "temperature" in sig else np.nan,
            "SoC [%]": soc[i],
            "HVAC": block["hvac_on"],
            "SegmentType": block["segment_type"]
        })

    time_offset += n
    prev_block = block

# === Save output ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"✅ Blended day saved to:\n{output_csv}")
print(f"📊 Segments used: {len(day_plan)}")
print(f"⏱️ Total duration: {df['Time [s]'].iloc[-1]} seconds")
