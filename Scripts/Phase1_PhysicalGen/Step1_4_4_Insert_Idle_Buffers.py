import numpy as np
import pandas as pd
import os
import random

# === Config ===
MIN_IDLE = 30  # seconds
MAX_IDLE = 60  # seconds

# === Paths ===
block_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_With_Idle_Buffers.csv"
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

# === Build day with idle insertion ===
time_offset = 0
rows = []
prev_block = None

for i, block_id in enumerate(day_plan):
    block = block_library[block_id]
    sig = block["signals"]
    n = len(sig["time"])

    # Add previous block content
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

    # Insert idle buffer unless it's the last block
    if i < len(day_plan) - 1:
        idle_duration = random.randint(MIN_IDLE, MAX_IDLE)
        last_voltage = sig["voltage"][-1]
        last_soc = sig["soc_displayed"][-1]
        last_temp = sig["temperature"][-1] if "temperature" in sig else np.nan
        hvac = random.random() < 0.3  # 30% chance HVAC is on

        for t in range(idle_duration):
            rows.append({
                "Time [s]": time_offset + t,
                "Current [A]": 0.0,
                "Voltage [V]": last_voltage,
                "Temperature [°C]": last_temp,
                "SoC [%]": last_soc,
                "HVAC": hvac,
                "SegmentType": "idle_buffer"
            })

        time_offset += idle_duration

# === Save to CSV ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"✅ Day with idle buffers saved to:\n{output_csv}")
print(f"📊 Total duration: {df['Time [s]'].iloc[-1]} seconds")
print(f"📦 Segments (including buffers): {len(day_plan)} + {len(day_plan) - 1} idle buffers")
