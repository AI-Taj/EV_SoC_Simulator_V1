import pandas as pd
import matplotlib.pyplot as plt

# === Load the file ===
csv_path = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Data\Synthetic_Days_Phase1\Day_With_Recharge.csv"
df = pd.read_csv(csv_path)

# === Plot ===
fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

axs[0].plot(df["Time [s]"], df["SoC [%]"], label="SoC [%]", linewidth=1.5)
axs[0].set_ylabel("SoC [%]")
axs[0].legend()
axs[0].grid(True)

axs[1].plot(df["Time [s]"], df["Current [A]"], label="Current [A]", color="tab:red", linewidth=1.5)
axs[1].set_ylabel("Current [A]")
axs[1].legend()
axs[1].grid(True)

axs[2].plot(df["Time [s]"], df["Voltage [V]"], label="Voltage [V]", color="tab:green", linewidth=1.5)
axs[2].set_ylabel("Voltage [V]")
axs[2].set_xlabel("Time [s]")
axs[2].legend()
axs[2].grid(True)

plt.tight_layout()

# === Save the figure ===
save_path = r"C:\Users\TAJ\Desktop\EV_SoC_Simulator_V1\Figures\Day_With_Recharge.png"
plt.savefig(save_path, dpi=300)
print(f"✅ Plot saved to: {save_path}")

plt.show()
