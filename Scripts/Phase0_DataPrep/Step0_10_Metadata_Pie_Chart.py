import os
import pandas as pd
import matplotlib.pyplot as plt

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Metadata_Filtered.csv')
plot_path = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_Metadata_PieChart.png')
os.makedirs(os.path.dirname(plot_path), exist_ok=True)

# === Load metadata
df = pd.read_csv(csv_path)

# === Count Trip Nature categories
counts = df['Trip Nature'].value_counts()

# === Plot pie chart
plt.figure(figsize=(6, 6))
colors = ['#66c2a5', '#fc8d62', '#8da0cb']
counts.plot.pie(autopct='%1.1f%%', startangle=90, counterclock=False, colors=colors)
plt.title('Trip Distribution by Nature', fontsize=14)
plt.ylabel('')  # Hide y-axis label
plt.tight_layout()
plt.savefig(plot_path, dpi=300)
plt.close()

print(f"✅ Pie chart saved to:\n{plot_path}")
