import numpy as np
import pandas as pd
import os

# === Paths ===
input_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Thresholds ===
THROTTLE_THR = 5.0      # %
VELOCITY_IDLE_THR = 2.0 # km/h
MIN_DRIVING = 30        # s
MIN_IDLE = 30           # s
MIN_REGEN = 10          # s

# === Load trip data ===
data = np.load(input_file, allow_pickle=True)
all_segments = {k: v.item() for k, v in data.items()}

rows = []

def classify(throttle, regen_signal, velocity, i):
    if throttle[i] > THROTTLE_THR:
        return "driving"
    elif regen_signal[i] == 1:
        return "regen"
    elif throttle[i] <= THROTTLE_THR and regen_signal[i] == 0 and velocity[i] <= VELOCITY_IDLE_THR:
        return "idle"
    else:
        return "uncategorized"

for trip_id, seg in all_segments.items():
    try:
        throttle = seg.get("Throttle [%]")
        regen = seg.get("Regenerative Braking Signal")
        velocity = seg.get("Velocity [km/h]")
        current = seg.get("current")
        voltage = seg.get("voltage")
        soc = seg.get("soc_displayed")
        time = seg.get("time")

        if any(x is None for x in [throttle, regen, velocity]):
            print(f"⚠️ Missing throttle or regen or velocity in {trip_id}, skipping.")
            continue

        state = None
        start_idx = 0

        for i in range(1, len(throttle)):
            curr_state = classify(throttle, regen, velocity, i)

            if curr_state != state or i == len(throttle) - 1:
                if state is not None:
                    end_idx = i
                    duration = end_idx - start_idx

                    valid = False
                    if state == "driving" and duration >= MIN_DRIVING:
                        valid = True
                    elif state == "idle" and duration >= MIN_IDLE:
                        valid = True
                    elif state == "regen" and duration >= MIN_REGEN:
                        valid = True

                    if valid:
                        row = {
                            "trip_id": trip_id,
                            "segment_type": state,
                            "start_idx": start_idx,
                            "end_idx": end_idx,
                            "duration_s": duration,
                            "mean_current": np.mean(current[start_idx:end_idx]) if current is not None else np.nan,
                            "mean_voltage": np.mean(voltage[start_idx:end_idx]) if voltage is not None else np.nan,
                            "max_current": np.max(current[start_idx:end_idx]) if current is not None else np.nan,
                            "min_current": np.min(current[start_idx:end_idx]) if current is not None else np.nan,
                        }
                        if soc is not None and len(soc) > end_idx:
                            row["soc_drop"] = soc[start_idx] - soc[end_idx]
                        rows.append(row)

                start_idx = i
                state = curr_state

    except Exception as e:
        print(f"❌ Failed on {trip_id}: {e}")

# === Save the result ===
df = pd.DataFrame(rows)
df.to_csv(output_csv, index=False)

print(f"\n✅ Saved updated segment metadata to:\n{output_csv}")
print(f"📊 Segment counts by type: {df['segment_type'].value_counts().to_dict()}")
