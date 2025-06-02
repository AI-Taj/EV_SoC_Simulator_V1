import numpy as np
import pandas as pd
import os

# === Paths ===
metadata_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.csv"
trip_data_npz = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"
output_npz = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\segment_blocks_library.npz"

# === Load inputs ===
df = pd.read_csv(metadata_csv)
trip_data = np.load(trip_data_npz, allow_pickle=True)
trip_segments = {k: v.item() for k, v in trip_data.items()}

# === Output structure ===
block_library = {}

# === Process each row ===
for idx, row in df.iterrows():
    trip_id = row["trip_id"]
    seg_type = row["segment_type"]
    hvac_on = row["hvac_on"]
    i_start = int(row["start_idx"])
    i_end = int(row["end_idx"])

    if trip_id not in trip_segments:
        print(f"⚠️ Trip not found: {trip_id}")
        continue

    signals = trip_segments[trip_id]

    block_id = f"{trip_id}_seg{idx:04d}"
    block_library[block_id] = {
        "trip_id": trip_id,
        "segment_type": seg_type,
        "hvac_on": bool(hvac_on),
        "duration_s": i_end - i_start,
        "signals": {
            k: v[i_start:i_end] for k, v in signals.items()
            if isinstance(v, np.ndarray) and len(v) > i_end
        }
    }

    print(f"✅ Block created: {block_id} [{seg_type}, HVAC={'ON' if hvac_on else 'OFF'}]")

# === Save the result ===
np.savez_compressed(output_npz, **block_library)
print(f"\n🎉 Segment block library saved to:\n{output_npz}")
print(f"📦 Total blocks stored: {len(block_library)}")
