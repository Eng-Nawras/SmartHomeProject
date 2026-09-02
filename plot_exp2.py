import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

summary = pd.read_csv('results/exp2_summary.csv')
summary['T'] = pd.to_numeric(summary['T'], errors='coerce')
summary['PDR_mean'] = pd.to_numeric(summary['PDR_mean'], errors='coerce')
summary['delay_mean_ms'] = pd.to_numeric(summary['delay_mean_ms'], errors='coerce')
summary['energy_per_node_J'] = pd.to_numeric(summary['energy_per_node_J'], errors='coerce')

fig, axes = plt.subplots(1, 3, figsize=(15, 4.5))

axes[0].plot(summary['T'], summary['PDR_mean'], marker='o', color='#2ca02c', linewidth=2)
axes[0].set_title('Experiment 2: PDR vs Reporting Interval')
axes[0].set_xlabel('Reporting interval T (s)')
axes[0].set_ylabel('PDR')
axes[0].set_ylim(0.99, 1.01)
axes[0].grid(True, linestyle='--', alpha=0.35)

axes[1].plot(summary['T'], summary['delay_mean_ms'], marker='s', color='#ff7f0e', linewidth=2)
axes[1].set_title('Experiment 2: Delay vs Reporting Interval')
axes[1].set_xlabel('Reporting interval T (s)')
axes[1].set_ylabel('Delay (ms)')
axes[1].grid(True, linestyle='--', alpha=0.35)

axes[2].plot(summary['T'], summary['energy_per_node_J'], marker='^', color='#9467bd', linewidth=2)
axes[2].set_title('Experiment 2: Energy per Node vs Reporting Interval')
axes[2].set_xlabel('Reporting interval T (s)')
axes[2].set_ylabel('Energy per node (J)')
axes[2].grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig('results/exp2_visualization.png', dpi=300)
print('Saved visualization to results/exp2_visualization.png')
