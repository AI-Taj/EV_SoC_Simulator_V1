import numpy as np
import pandas as pd
import os
import random

# === Config ===
RAMP_DURATION = 5  # seconds

# === Paths ===
block_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_With_Interpolated_Ramps.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Load block data ===
block_data = np.load(block_file, allow_pickle=True)
block_library = {k: v.item() for k, v in block_data.items()}

# === Select blocks ===
driving_blocks = [k for k, v in block_library.items() if v["segment_type"] == "driving"]
idle_blocks = [k for k, v in block_library.items() if v["segment_type"] == "idle"]
regen_blocks = [k for k, v in block_library.items() if v["segment_type"] == "regen"]

random.seed(42)
day_plan = []
day_plan += random.sample(driving_blocks, 3)
day_plan += random.sample(idle_blocks, 1)
day_plan += random.sample(driving_blocks, 2)
if regen_blocks:
    day_plan += random.sample(regen_blocks, 1)
day_plan += random.sample(idle_blocks, 1)

# === Build day with interpolated ramps ===
time_offset = 0
rows = []
prev_block = None

for i, block_id in enumerate(day_plan):
    block = block_library[block_id]
    sig = block["signals"]
    n = len(sig["time"])

    # Append current block
    for j in range(n):
        rows.append({
            "Time [s]": time_offset + j,
            "Current [A]": sig["current"][j],
            "Voltage [V]": sig["voltage"][j],
            "Temperature [°C]": sig["temperature"][j] if "temperature" in sig else np.nan,
            "SoC [%]": sig["soc_displayed"][j],
            "HVAC": block["hvac_on"],
            "SegmentType": block["segment_type"]
        })

    time_offset += n

    # Insert interpolated ramp
    if prev_block:
        end_prev = prev_block["signals"]
        start_curr = sig

        def interp(val_a, val_b):
            return np.linspace(val_a, val_b, RAMP_DURATION)

        ramp_soc = interp(end_prev["soc_displayed"][-1], start_curr["soc_displayed"][0])
        ramp_current = interp(end_prev["current"][-1], start_curr["current"][0])
        ramp_voltage = interp(end_prev["voltage"][-1], start_curr["voltage"][0])
        ramp_temp = interp(end_prev["temperature"][-1], start_curr["temperature"][0]) \
            if "temperature" in end_prev and "temperature" in start_curr else [np.nan] * RAMP_DURATION

        for k in range(RAMP_DURATION):
            rows.append({
                "Time [s]": time_offset + k,
                "Current [A]": ramp_current[k],
                "Voltage [V]": ramp_voltage[k],
                "Temperature [°C]": ramp_temp[k],
                "SoC [%]": ramp_soc[k],
                "HVAC": random.random() < 0.3,
                "SegmentType": "ramp"
            })

        time_offset += RAMP_DURATION

    prev_block = block

# === Save to CSV ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"✅ Day with interpolated ramps saved to:\n{output_csv}")
print(f"📊 Total duration: {df['Time [s]'].iloc[-1]} seconds")
print(f"📦 Segments: {len(day_plan)} + {len(day_plan) - 1} ramps")
