import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy.stats import norm

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
plot_dir = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_TripStats_Visuals')
os.makedirs(plot_dir, exist_ok=True)

# === Load Data
df = pd.read_csv(csv_path)

# === Helpers
def sanitize_filename(text):
    return (text.replace(" ", "_").replace("[", "").replace("]", "").replace("/", "_")
            .replace("(", "").replace(")", "").replace("%", "pct"))

def savefig(title):
    safe_title = sanitize_filename(title)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"{safe_title}.png"), dpi=300)
    plt.close()

# === 1. Histograms + Gaussian Fit
features_hist = ['Duration [s]', 'ΔSoC [%]', 'Energy Used [Wh]', 'Regen Time [s]', 'Mean HVAC Power [kW]']
for feat in features_hist:
    if feat in df.columns:
        data = df[feat].dropna()
        plt.figure(figsize=(6, 4))
        sns.histplot(data, bins=20, kde=False, color='skyblue', stat="density", label="Histogram")

        # Gaussian fit
        mu, std = norm.fit(data)
        x = np.linspace(data.min(), data.max(), 100)
        plt.plot(x, norm.pdf(x, mu, std), 'r--', label=f'Gaussian Fit\nμ={mu:.2f}, σ={std:.2f}')
        plt.title(f"Histogram + Gaussian Fit: {feat}")
        plt.legend()
        savefig(f"Hist_Gauss_{feat}")

# === 2. Boxplots (unchanged)
for feat in features_hist:
    if feat in df.columns:
        plt.figure(figsize=(6, 4))
        sns.boxplot(x=df[feat], color='lightgreen')
        plt.title(f"Boxplot of {feat}")
        savefig(f"Boxplot_{feat}")

# === 3. Scatter Plots
scatter_pairs = [
    ('ΔSoC [%]', 'Energy Used [Wh]'),
    ('Max Speed [km/h]', 'Energy Used [Wh]'),
    ('Duration [s]', 'ΔSoC [%]')
]

for x, y in scatter_pairs:
    if x in df.columns and y in df.columns:
        plt.figure(figsize=(6, 4))
        sns.scatterplot(data=df, x=x, y=y, hue='Trip ID', palette='viridis', legend=False)
        plt.title(f"{y} vs {x}")
        savefig(f"Scatter_{x}_vs_{y}")

# === 4. Correlation Heatmap
numeric_df = df.select_dtypes(include='number')
plt.figure(figsize=(10, 8))
corr = numeric_df.corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title("Correlation Heatmap of Trip-Level Features")
savefig("Correlation_Heatmap")

# === 5. Radar Charts for 5 sample trips
radar_features = ['Duration [s]', 'ΔSoC [%]', 'Energy Used [Wh]', 'Regen Time [s]', 'Mean HVAC Power [kW]']
df_radar = df.dropna(subset=radar_features).copy()
selected_trips = df_radar.sample(n=5, random_state=42) if len(df_radar) >= 5 else df_radar

# Normalize values (min-max scaling)
normalized = selected_trips.copy()
for col in radar_features:
    min_val = df_radar[col].min()
    max_val = df_radar[col].max()
    normalized[col] = (df_radar[col] - min_val) / (max_val - min_val)

# Radar chart setup
labels = radar_features
num_vars = len(labels)
angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

# Repeat the first to close the loop
angles += angles[:1]

plt.figure(figsize=(6, 6))
for idx, row in normalized.iterrows():
    values = row[radar_features].tolist()
    values += values[:1]  # close the loop
    plt.polar(angles, values, label=row['Trip ID'])

plt.xticks(angles[:-1], radar_features, fontsize=8)

plt.xticks(angles[:-1], radar_features, fontsize=8)
plt.title("Radar Comparison of 5 Sample Trips")
plt.legend(loc='upper right', bbox_to_anchor=(1.2, 1.1))
savefig("Radar_Trip_Comparison")

print(f"\n✅ All extended visualizations (Gaussian, Radar, Summary) saved to:\n{plot_dir}")
