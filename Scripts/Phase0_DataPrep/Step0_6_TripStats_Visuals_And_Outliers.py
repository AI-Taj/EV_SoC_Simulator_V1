import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
csv_path = os.path.join(base_path, 'Validation', 'Reports', 'Phase0_Trip_Statistics.csv')
plot_dir = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_TripStats_Visuals')
os.makedirs(plot_dir, exist_ok=True)

# === Load trip statistics
df = pd.read_csv(csv_path)

# === Helpers
def sanitize_filename(text):
    return (
        text.replace(" ", "_")
            .replace("[", "")
            .replace("]", "")
            .replace("/", "_")
            .replace("(", "")
            .replace(")", "")
            .replace("%", "pct")
    )

def savefig(title):
    safe_title = sanitize_filename(title)
    plt.tight_layout()
    plt.savefig(os.path.join(plot_dir, f"{safe_title}.png"), dpi=300)
    plt.close()

# === 1. Histograms
features_hist = ['Duration [s]', 'ΔSoC [%]', 'Energy Used [Wh]', 'Regen Time [s]', 'Mean HVAC Power [kW]']
for feat in features_hist:
    if feat in df.columns:
        plt.figure(figsize=(6, 4))
        sns.histplot(df[feat].dropna(), kde=True, bins=20, color='skyblue')
        plt.title(f"Histogram of {feat}")
        savefig(f"Hist_{feat}")

# === 2. Boxplots for outlier detection
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

print(f"\n✅ All visual summary plots saved to:\n{plot_dir}")
