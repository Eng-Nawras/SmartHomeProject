import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

summary = pd.read_csv('results/exp5_summary.csv')
summary['L'] = pd.to_numeric(summary['L'], errors='coerce')
summary['PDR_mean'] = pd.to_numeric(summary['PDR_mean'], errors='coerce')
summary['delay_mean_ms'] = pd.to_numeric(summary['delay_mean_ms'], errors='coerce')
summary['mac_frames_per_app_pkt'] = pd.to_numeric(summary['mac_frames_per_app_pkt'], errors='coerce')
summary['energy_per_packet_mJ'] = pd.to_numeric(summary['energy_per_packet_mJ'], errors='coerce')

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

axes[0].plot(summary['L'], summary['PDR_mean'], marker='o', color='#17becf', linewidth=2)
axes[0].set_title('Experiment 5: PDR vs Packet Size')
axes[0].set_xlabel('Packet size L (B)')
axes[0].set_ylabel('PDR')
axes[0].set_ylim(0.95, 1.01)
axes[0].grid(True, linestyle='--', alpha=0.35)

axes[1].plot(summary['L'], summary['delay_mean_ms'], marker='s', color='#bcbd22', linewidth=2)
axes[1].set_title('Experiment 5: Delay vs Packet Size')
axes[1].set_xlabel('Packet size L (B)')
axes[1].set_ylabel('Delay (ms)')
axes[1].grid(True, linestyle='--', alpha=0.35)

axes[2].plot(summary['L'], summary['energy_per_packet_mJ'], marker='^', color='#8c564b', linewidth=2)
axes[2].set_title('Experiment 5: Energy per Packet vs Packet Size')
axes[2].set_xlabel('Packet size L (B)')
axes[2].set_ylabel('Energy per packet (mJ)')
axes[2].grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig('results/exp5_visualization.png', dpi=300)
print('Saved visualization to results/exp5_visualization.png')
