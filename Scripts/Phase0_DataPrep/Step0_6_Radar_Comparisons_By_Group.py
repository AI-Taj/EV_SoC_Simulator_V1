import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
plot_dir = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_TripStats_Visuals', 'Radar_Groups')
os.makedirs(plot_dir, exist_ok=True)

# === Load Data
df = pd.read_csv(csv_path)

# === Metrics to include
radar_metrics = ['Duration [s]', 'ΔSoC [%]', 'Energy Used [Wh]', 'Regen Time [s]', 'Mean HVAC Power [kW]']
df = df.dropna(subset=radar_metrics)

# === Global normalization range
min_vals = df[radar_metrics].min()
max_vals = df[radar_metrics].max()

def normalize(values):
    return [(v - min_vals[c]) / (max_vals[c] - min_vals[c]) if pd.notnull(v) else 0
            for v, c in zip(values, radar_metrics)]

def plot_radar(profiles_dict, title, filename):
    labels = radar_metrics
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(6, 6))
    for label, profile in profiles_dict.items():
        values = normalize(profile)
        values += values[:1]  # close the loop
        plt.polar(angles, values, label=label)

    plt.xticks(angles[:-1], labels, fontsize=8)
    plt.title(title)
    plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, filename), dpi=300)
    plt.close()

# === 1. TripA vs TripB
df_A = df[df['Trip ID'].str.startswith("TripA")]
df_B = df[df['Trip ID'].str.startswith("TripB")]
if not df_A.empty and not df_B.empty:
    profiles = {
        "TripA (avg)": df_A[radar_metrics].mean().tolist(),
        "TripB (avg)": df_B[radar_metrics].mean().tolist()
    }
    plot_radar(profiles, "Average Profile: TripA vs TripB", "Radar_TripA_vs_TripB.png")

# === 2. Short vs Long Trips
df_short = df[df['Duration [s]'] < 1000]
df_long = df[df['Duration [s]'] > 2000]
if not df_short.empty and not df_long.empty:
    profiles = {
        "Short Trips": df_short[radar_metrics].mean().tolist(),
        "Long Trips": df_long[radar_metrics].mean().tolist()
    }
    plot_radar(profiles, "Short vs Long Trips", "Radar_Short_vs_Long.png")

# === 3. High vs Low Energy Trips
df_sorted_energy = df.sort_values('Energy Used [Wh]')
df_low_energy = df_sorted_energy.head(5)
df_high_energy = df_sorted_energy.tail(5)
if not df_low_energy.empty and not df_high_energy.empty:
    profiles = {
        "Low Energy Trips": df_low_energy[radar_metrics].mean().tolist(),
        "High Energy Trips": df_high_energy[radar_metrics].mean().tolist()
    }
    plot_radar(profiles, "High vs Low Energy Trips", "Radar_High_vs_Low_Energy.png")

# === 4. Charging/Idle vs Discharging Trips
df_discharge = df[df['ΔSoC [%]'] < -2]
df_charge_or_idle = df[df['ΔSoC [%]'] >= 0]
if not df_discharge.empty and not df_charge_or_idle.empty:
    profiles = {
        "Discharging Trips": df_discharge[radar_metrics].mean().tolist(),
        "Charging or Idle Trips": df_charge_or_idle[radar_metrics].mean().tolist()
    }
    plot_radar(profiles, "Charging vs Discharging Trips", "Radar_Charging_vs_Discharging.png")

# === 5. High vs Low Regen Trips
df_sorted_regen = df.sort_values('Regen Time [s]')
df_low_regen = df_sorted_regen.head(5)
df_high_regen = df_sorted_regen.tail(5)
if not df_low_regen.empty and not df_high_regen.empty:
    profiles = {
        "Low Regen Trips": df_low_regen[radar_metrics].mean().tolist(),
        "High Regen Trips": df_high_regen[radar_metrics].mean().tolist()
    }
    plot_radar(profiles, "High vs Low Regeneration Trips", "Radar_High_vs_Low_Regen.png")

print(f"\n✅ Fixed radar comparison plots saved to:\n{plot_dir}")
