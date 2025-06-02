import os
import pandas as pd
import matplotlib.pyplot as plt

# === Script Name: Step0_Visual_Fig1_Downsampling_Continuity.py

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
trip_raw = os.path.join(base_path, 'Data', 'Raw_Data', 'TripA', 'TripA01.csv')
trip_downsampled = os.path.join(base_path, 'Data', 'Processed_Trips', 'TripA_1s', 'TripA01_d1s.csv')
fig_out = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_Figure1_Downsampling_Continuity.png')
os.makedirs(os.path.dirname(fig_out), exist_ok=True)

# === Load raw file (detect separator)
sep = ";" if pd.read_csv(trip_raw, nrows=1, sep=";", encoding='ISO-8859-1').shape[1] > 1 else ","
df_raw = pd.read_csv(trip_raw, sep=sep, encoding='ISO-8859-1')
df_down = pd.read_csv(trip_downsampled)

# === Ensure columns exist
assert 'Time [s]' in df_raw.columns and 'Battery Current [A]' in df_raw.columns, "Check column names in raw file"
assert 'Time [s]' in df_down.columns and 'Battery Current [A]' in df_down.columns, "Check column names in downsampled file"

# === Plotting
plt.figure(figsize=(10, 6))

# Top: Raw signal
plt.subplot(2, 1, 1)
plt.plot(df_raw['Time [s]'], df_raw['Battery Current [A]'], color='tab:blue', linewidth=0.8)
plt.title('Raw Battery Current [A] – Irregular Timestamps')
plt.ylabel('Current [A]')
plt.grid(True)

# Bottom: Downsampled signal
plt.subplot(2, 1, 2)
plt.step(df_down['Time [s]'], df_down['Battery Current [A]'], color='tab:orange', linewidth=1, where='post')
plt.title('Downsampled Battery Current [A] – 1s Regular Intervals')
plt.xlabel('Time [s]')
plt.ylabel('Current [A]')
plt.grid(True)

plt.tight_layout()
plt.savefig(fig_out, dpi=300)
plt.close()

print(f"✅ Figure 1 saved to:\n{fig_out}")
