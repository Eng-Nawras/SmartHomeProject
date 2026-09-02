import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

summary = pd.read_csv('results/exp1_summary.csv')
summary['N'] = pd.to_numeric(summary['N'], errors='coerce')
summary['PDR_mean'] = pd.to_numeric(summary['PDR_mean'], errors='coerce')
summary['delay_mean_ms'] = pd.to_numeric(summary['delay_mean_ms'], errors='coerce')

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

axes[0].plot(summary['N'], summary['PDR_mean'], marker='o', linewidth=2, color='#1f77b4')
axes[0].set_title('Experiment 1: PDR vs Number of Nodes')
axes[0].set_xlabel('Number of Nodes (N)')
axes[0].set_ylabel('PDR')
axes[0].set_ylim(0.95, 1.05)
axes[0].grid(True, linestyle='--', alpha=0.4)

axes[1].plot(summary['N'], summary['delay_mean_ms'], marker='s', linewidth=2, color='#d62728')
axes[1].set_title('Experiment 1: End-to-End Delay vs Number of Nodes')
axes[1].set_xlabel('Number of Nodes (N)')
axes[1].set_ylabel('Delay (ms)')
axes[1].grid(True, linestyle='--', alpha=0.4)

plt.tight_layout()
plt.savefig('results/exp1_visualization.png', dpi=300)
print('Saved visualization to results/exp1_visualization.png')
