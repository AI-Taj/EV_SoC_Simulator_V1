import os
import pandas as pd

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
tripA_1s = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_1s')
tripB_1s = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripB_1s')
output_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# === Features to extract
def analyze_trip(file_path, trip_id):
    try:
        df = pd.read_csv(file_path)

        # Check minimum required columns
        if 'Time [s]' not in df.columns or 'SoC [%]' not in df.columns:
            return None

        duration = df['Time [s]'].max() - df['Time [s]'].min()
        soc_start = df['SoC [%]'].iloc[0]
        soc_end = df['SoC [%]'].iloc[-1]
        delta_soc = soc_end - soc_start

        mean_speed = df['Velocity [km/h]'].mean() if 'Velocity [km/h]' in df else None
        max_speed = df['Velocity [km/h]'].max() if 'Velocity [km/h]' in df else None

        mean_current = df['Battery Current [A]'].mean() if 'Battery Current [A]' in df else None
        mean_voltage = df['Battery Voltage [V]'].mean() if 'Battery Voltage [V]' in df else None

        energy_wh = None
        if 'Battery Current [A]' in df and 'Battery Voltage [V]' in df:
            df['Power_W'] = df['Battery Current [A]'] * df['Battery Voltage [V]']
            energy_wh = df['Power_W'].sum() / 3600  # 1s resolution

        regen_time = df['Regenerative Braking Signal'].sum() if 'Regenerative Braking Signal' in df else None

        hvac_power = df[['Heating Power CAN [kW]', 'AirCon Power [kW]']].mean().sum(skipna=True) \
            if 'Heating Power CAN [kW]' in df and 'AirCon Power [kW]' in df else None

        return {
            'Trip ID': trip_id,
            'Duration [s]': duration,
            'SoC Start [%]': soc_start,
            'SoC End [%]': soc_end,
            'ΔSoC [%]': delta_soc,
            'Mean Speed [km/h]': mean_speed,
            'Max Speed [km/h]': max_speed,
            'Mean Voltage [V]': mean_voltage,
            'Mean Current [A]': mean_current,
            'Energy Used [Wh]': energy_wh,
            'Regen Time [s]': regen_time,
            'Mean HVAC Power [kW]': hvac_power
        }
    except Exception as e:
        print(f"❌ {trip_id} failed: {e}")
        return None

# === Batch Process
all_stats = []

for i in range(1, 33):
    f = f"TripA{str(i).zfill(2)}_d1s.csv"
    path = os.path.join(tripA_1s, f)
    if os.path.exists(path):
        stats = analyze_trip(path, f"TripA{str(i).zfill(2)}")
        if stats:
            all_stats.append(stats)

for i in range(1, 39):
    f = f"TripB{str(i).zfill(2)}_d1s.csv"
    path = os.path.join(tripB_1s, f)
    if os.path.exists(path):
        stats = analyze_trip(path, f"TripB{str(i).zfill(2)}")
        if stats:
            all_stats.append(stats)

# === Save output
df_stats = pd.DataFrame(all_stats)
df_stats.to_csv(output_path, index=False)
print(f"\n✅ Trip-level statistics saved to:\n{output_path}")
