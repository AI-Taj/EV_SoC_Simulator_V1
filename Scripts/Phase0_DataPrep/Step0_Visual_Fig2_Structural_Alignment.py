import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.table import Table

# === Paths
base_path = r'C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1'
fig_path = os.path.join(base_path, 'Validation', 'Plots', 'Phase0_Figure2_Structural_Alignment.png')
os.makedirs(os.path.dirname(fig_path), exist_ok=True)

# === Define fake raw headers (with issues)
raw_headers = [
    "Cabin Temp [°C",        # malformed
    "Velocity [kmh]",        # wrong unit
    "SoC [%]",               # OK
    "Throttle",              # missing unit
    "Reg Braking ",          # trailing space
    "Power Draw (W)"         # extra/unknown
]

# === Define reference standardized headers
ref_headers = [
    "Cabin Temperature Sensor [°C]",
    "Velocity [km/h]",
    "SoC [%]",
    "Throttle [%]",
    "Regenerative Braking Signal",
    "Power Draw [W]"  # assumed mapped
]

# === Build simple data frames (1 row of dummy values)
raw_df = pd.DataFrame([["..."] * len(raw_headers)], columns=raw_headers)
std_df = pd.DataFrame([["..."] * len(ref_headers)], columns=ref_headers)

# === Create figure
fig, axes = plt.subplots(2, 1, figsize=(12, 4))
fig.suptitle("Figure 2 – Structural Alignment of Trip Files", fontsize=14)

def render_table(ax, df, title, color='lightgrey'):
    ax.set_axis_off()
    tbl = Table(ax, bbox=[0, 0, 1, 1])
    ncols = len(df.columns)
    width = 1.0 / ncols
    height = 1.0

    # Add headers
    for i, col in enumerate(df.columns):
        tbl.add_cell(0, i, width, height, text=col, loc='center', facecolor=color, fontproperties={'size': 8})

    # Add values
    for i, val in enumerate(df.iloc[0]):
        tbl.add_cell(1, i, width, height, text=val, loc='center', facecolor='white')

    ax.add_table(tbl)
    ax.set_title(title, fontsize=11, pad=12)

# === Render both tables
render_table(axes[0], raw_df, "Before Alignment: Raw Trip File with Inconsistent Columns", color="#fddbc7")
render_table(axes[1], std_df, "After Alignment: Matched to Reference Header Schema", color="#d1e5f0")

plt.tight_layout()
plt.subplots_adjust(top=0.85)
plt.savefig(fig_path, dpi=300)
plt.close()

print(f"✅ Figure 2 saved to:\n{fig_path}")
