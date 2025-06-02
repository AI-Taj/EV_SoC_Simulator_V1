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

# === Initialize flags
df['Use in Model'] = 'Yes'
df['Comment'] = 'Normal Drive'

# === Apply filtering rules
df.loc[df['ΔSoC [%]'] >= 0, ['Use in Model', 'Comment']] = ['No', 'Likely Charging or Idle']
df.loc[df['Duration [s]'] < 300, ['Use in Model', 'Comment']] = ['No', 'Too short']
df.loc[df['Energy Used [Wh]'] < 100, ['Use in Model', 'Comment']] = ['No', 'Too little energy']

# === Save output
df.to_csv(meta_out, index=False)
print(f"✅ Metadata with filtering saved to:\n{meta_out}")
