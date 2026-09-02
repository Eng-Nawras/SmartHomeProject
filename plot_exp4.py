import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

summary = pd.read_csv('results/exp4_comparison.csv')
summary['I'] = pd.to_numeric(summary['I'], errors='coerce')
summary['PDR_mean'] = pd.to_numeric(summary['PDR_mean'], errors='coerce')
summary['latency_mean_ms'] = pd.to_numeric(summary['latency_mean_ms'], errors='coerce')

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

for strategy, group in summary.groupby('strategy'):
    axes[0].plot(group['I'], group['PDR_mean'], marker='o', linewidth=2, label=strategy)
    axes[1].plot(group['I'], group['latency_mean_ms'], marker='s', linewidth=2, label=strategy)

axes[0].set_title('Experiment 4: PDR Comparison')
axes[0].set_xlabel('Interval I (s)')
axes[0].set_ylabel('PDR')
axes[0].legend()
axes[0].grid(True, linestyle='--', alpha=0.35)

axes[1].set_title('Experiment 4: Latency Comparison')
axes[1].set_xlabel('Interval I (s)')
axes[1].set_ylabel('Latency (ms)')
axes[1].legend()
axes[1].grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig('results/exp4_visualization.png', dpi=300)
print('Saved visualization to results/exp4_visualization.png')
