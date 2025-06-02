import numpy as np
import pandas as pd
import os

# === Paths ===
input_file = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segments_TA_TB_1s.npz"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Parsed\trip_segment_tags_metadata.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# === Thresholds ===
THROTTLE_THR = 5.0        # Throttle > 5% = driving
VELOCITY_IDLE_THR = 2.0   # Velocity ≤ 2 km/h = idle
AIRCON_THR = 0.5          # AirCon Power > 0.5 kW considered active
HVAC_RATIO_THR = 0.8      # 80% of segment must have HVAC active
MIN_DRIVING = 30          # s
MIN_IDLE = 30             # s
MIN_REGEN = 10            # s

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
        # Correct signal keys from Step 1.1 npz structure
        throttle = seg.get("throttle")
        regen = seg.get("regen_signal")
        velocity = seg.get("velocity")
        aircon = seg.get("aircon_power")
        current = seg.get("current")
        voltage = seg.get("voltage")
        soc = seg.get("soc_displayed")
        time = seg.get("time")

        if any(x is None for x in [throttle, regen, velocity, aircon]):
            print(f"⚠️ Missing critical signals in {trip_id}, skipping.")
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
                        segment_aircon = aircon[start_idx:end_idx]
                        hvac_ratio = np.mean(segment_aircon > AIRCON_THR)
                        hvac_on = hvac_ratio >= HVAC_RATIO_THR

                        row = {
                            "trip_id": trip_id,
                            "segment_type": state,
                            "hvac_on": hvac_on,
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
        print(f"❌ Error on trip {trip_id}: {e}")

# === Save output ===
df = pd.DataFrame(rows)

if df.empty:
    print("\n⚠️ No valid segments were found! Check thresholds or signal content.")
else:
    df.to_csv(output_csv, index=False)
    print(f"\n✅ Saved segment metadata with HVAC tag to:\n{output_csv}")
    print(f"📊 Segment counts:\n{df['segment_type'].value_counts()}")
    print(f"🔥 HVAC ON segments: {df['hvac_on'].sum()} / {len(df)}")
