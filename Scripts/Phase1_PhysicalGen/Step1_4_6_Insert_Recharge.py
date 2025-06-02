import pandas as pd
import numpy as np
import os

# === Config ===
soc_floor = 25.0         # recharge if SoC < threshold
target_soc = 90.0        # target SoC
battery_capacity_kWh = 40.0
charging_current = 30.0  # A (constant)
nominal_voltage = 360.0
internal_resistance = 0.05  # ohm
charging_efficiency = 0.95  # η

# === Input/output ===
input_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_With_Interpolated_Ramps.csv"
output_csv = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_With_Recharge.csv"
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

df = pd.read_csv(input_csv)
last_soc = df["SoC [%]"].iloc[-1]

# === Recharge condition ===
if last_soc >= soc_floor:
    print(f"🔋 SoC = {last_soc:.2f}% ≥ threshold ({soc_floor}%) → no recharge needed.")
    df.to_csv(output_csv, index=False)
    print(f"✅ Copied original file to:\n{output_csv}")
else:
    print(f"🔋 SoC = {last_soc:.2f}% < threshold ({soc_floor}%) → recharge triggered.")

    soc_start = last_soc
    soc_target = target_soc
    delta_soc = soc_target - soc_start

    # Energy needed in kWh
    energy_needed_kWh = battery_capacity_kWh * (delta_soc / 100)
    time_hours = energy_needed_kWh / (charging_current * nominal_voltage / 1000 * charging_efficiency)
    time_seconds = int(time_hours * 3600)

    print(f"⚡ Energy needed: {energy_needed_kWh:.2f} kWh → {time_seconds} seconds at {charging_current} A")

    last_voltage = df["Voltage [V]"].iloc[-1]
    last_temp = df["Temperature [°C]"].iloc[-1]
    time_start = df["Time [s]"].iloc[-1] + 1

    recharge_rows = []
    for t in range(time_seconds):
        soc = soc_start + (delta_soc * t / time_seconds)
        voltage = nominal_voltage + charging_current * internal_resistance

        recharge_rows.append({
            "Time [s]": time_start + t,
            "Current [A]": -charging_current,  # negative = charging
            "Voltage [V]": voltage,
            "Temperature [°C]": last_temp,
            "SoC [%]": soc,
            "HVAC": False,
            "SegmentType": "recharge"
        })

    df_recharge = pd.DataFrame(recharge_rows)
    df_final = pd.concat([df, df_recharge], ignore_index=True)
    df_final.to_csv(output_csv, index=False)

    print(f"✅ Recharge block added. Total new duration: {df_final['Time [s]'].iloc[-1]} s")
    print(f"📁 File saved to:\n{output_csv}")
