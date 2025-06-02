import numpy as np
import pandas as pd
import os

# === Input file ===
input_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Thresholds ===
IDLE_THR = 1.5     # A
DRIVING_THR = 3.0  # A
CHARGING_THR = -3.0  # A
MIN_SEGMENT_LEN = 30  # s (except regen)

# === Load all trips ===
data = np.load(input_file, allow_pickle=True)
all_segments = {k: v.item() for k, v in data.items()}

rows = []

for trip_id, seg in all_segments.items():
    current = seg["current"]
    voltage = seg["voltage"]
    soc = seg["soc_displayed"]
    time = seg["time"]

    if len(current) < 2:
        continue

    # --- Segment classification by scanning ---
    state = None
    start_idx = 0

    def classify(i):
        if abs(current[i]) < IDLE_THR:
            return "idle"
        elif current[i] > DRIVING_THR:
            return "driving"
        elif current[i] < CHARGING_THR:
            return "charging"
        elif current[i] < 0:
            return "regen"
        else:
            return "uncategorized"

    for i in range(1, len(current)):
        curr_state = classify(i)

        # If state changes or end of data
        if curr_state != state or i == len(current) - 1:
            if state is not None:
                end_idx = i
                duration = end_idx - start_idx
                if duration >= MIN_SEGMENT_LEN or state == "regen":
                    row = {
                        "trip_id": trip_id,
                        "start_idx": start_idx,
                        "end_idx": end_idx,
                        "duration_s": duration,
                        "segment_type": state,
                        "mean_current": np.mean(current[start_idx:end_idx]),
                        "mean_voltage": np.mean(voltage[start_idx:end_idx]),
                        "max_current": np.max(current[start_idx:end_idx]),
                        "min_current": np.min(current[start_idx:end_idx]),
                    }
                    if soc is not None and len(soc) > end_idx:
                        row["soc_drop"] = soc[start_idx] - soc[end_idx]
                    rows.append(row)
            # Reset state
            start_idx = i
            state = curr_state

# === Save to CSV ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)
print(f"✅ Segment classification saved to:\n{output_csv}")
print(f"📊 Total segments tagged: {len(df)}")
