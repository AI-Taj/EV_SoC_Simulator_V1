import pandas as pd
import matplotlib.pyplot as plt

# === Load the aligned synthetic day CSV ===
csv_path = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_SoC_Aligned.csv"
df = pd.read_csv(csv_path)

# === Create plot ===
fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

# SoC Plot
axs[0].plot(df["Time [s]"], df["SoC [%]"], label="SoC [%]", linewidth=1.5)
axs[0].set_ylabel("SoC [%]")
axs[0].legend()
axs[0].grid(True)

# Current Plot
axs[1].plot(df["Time [s]"], df["Current [A]"], label="Current [A]", color="tab:red", linewidth=1.5)
axs[1].set_ylabel("Current [A]")
axs[1].legend()
axs[1].grid(True)

# Voltage Plot
axs[2].plot(df["Time [s]"], df["Voltage [V]"], label="Voltage [V]", color="tab:green", linewidth=1.5)
axs[2].set_ylabel("Voltage [V]")
axs[2].set_xlabel("Time [s]")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()

# === Save plot ===
save_path = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Figures\Day_SoC_Aligned.png"
plt.savefig(save_path, dpi=300)
print(f"✅ Saved 300 dpi plot to:\n{save_path}")

plt.show()
