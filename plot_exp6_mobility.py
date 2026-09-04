import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('results/exp6_mobility_summary.csv')

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

axes[0].plot(df['speed'], df['link_PDR_mean'], marker='o', color='tab:blue')
axes[0].set_title('Experiment 6 (Bonus): Link PDR vs Wearable Speed')
axes[0].set_xlabel('Speed (m/s)')
axes[0].set_ylabel('Link PDR')
axes[0].grid(True, alpha=0.3)

axes[1].plot(df['speed'], df['delay_mean_ms'], marker='o', color='tab:orange')
axes[1].set_title('Experiment 6 (Bonus): Delay vs Wearable Speed')
axes[1].set_xlabel('Speed (m/s)')
axes[1].set_ylabel('Delay (ms)')
axes[1].grid(True, alpha=0.3)

axes[2].plot(df['speed'], df['energy_per_packet_mJ'], marker='o', color='tab:purple')
axes[2].set_title('Experiment 6 (Bonus): Energy per Packet vs Speed')
axes[2].set_xlabel('Speed (m/s)')
axes[2].set_ylabel('Energy per packet (mJ)')
axes[2].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/exp6_mobility_visualization.png', dpi=300)
print("Saved results/exp6_mobility_visualization.png")
