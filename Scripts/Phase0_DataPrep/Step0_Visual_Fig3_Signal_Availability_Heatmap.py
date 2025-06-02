import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
tripA_path = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_Cleaned')
tripB_path = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripB_Cleaned')
plot_path = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_Figure3_Signal_Availability.png')
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

# === Define essential canonical features
essential_features = [
    "Time [s]",
    "SoC [%]",
    "displayed SoC [%]",
    "Battery Voltage [V]",
    "Battery Current [A]",
    "Battery Temperature [°C]",
    "Velocity [km/h]",
    "Throttle [%]",
    "Motor Torque [Nm]",
    "Regenerative Braking Signal"
]

# === Collect cleaned trip files
trip_files = []
for prefix, folder, count in [('TripA', tripA_path, 32), ('TripB', tripB_path, 38)]:
    for i in range(1, count + 1):
        fname = f"{prefix}{str(i).zfill(2)}_cleaned.csv"
        full_path = os.path.join(folder, fname)
        if os.path.exists(full_path):
            trip_files.append((f"{prefix}{str(i).zfill(2)}", full_path))

# === Build binary presence matrix
presence_df = pd.DataFrame(0, index=essential_features, columns=[trip_id for trip_id, _ in trip_files])

for trip_id, path in trip_files:
    df = pd.read_csv(path, nrows=1)
    present_cols = set(df.columns)
    for feature in essential_features:
        if feature in present_cols:
            presence_df.loc[feature, trip_id] = 1

# === Plot heatmap
plt.figure(figsize=(max(10, len(trip_files) * 0.25), len(essential_features) * 0.5))
sns.heatmap(presence_df, cmap='Greens', cbar=False, linewidths=0.4, linecolor='lightgray', vmin=0, vmax=1)
plt.title("Figure 3 – Signal Availability Matrix Across All Trips", fontsize=14)
plt.xlabel("Trip ID")
plt.ylabel("Essential Signal Name")
plt.xticks(rotation=90, fontsize=6)
plt.yticks(fontsize=8)
plt.tight_layout()
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"✅ Corrected Figure 3 saved to:\n{plot_path}")
