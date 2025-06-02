import os
import pandas as pd

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
stats_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
meta_out = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Metadata_Filtered.csv')

# === Load statistics
df = pd.read_csv(stats_path)

# === Add group: A or B
df['Group'] = df['Trip ID'].str.extract(r'Trip([AB])')[0]

# === Label trip nature (descriptive only)
df['Trip Nature'] = 'Driving'
df.loc[df['ΔSoC [%]'] >= 0, 'Trip Nature'] = 'Charging or Idle'
df.loc[df['Duration [s]'] < 180, 'Trip Nature'] = 'Too Short'

# === All trips included
df['Use in Model'] = 'Yes'
df['Comment'] = 'Retained for global characterization'

# === Save output
df.to_csv(meta_out, index=False)
print(f"✅ Metadata saved with no exclusions at:\n{meta_out}")
