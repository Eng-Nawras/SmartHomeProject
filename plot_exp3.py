import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

summary = pd.read_csv('results/exp3_summary.csv')
summary['BG'] = pd.to_numeric(summary['BG'], errors='coerce')
summary['crit_PDR_mean'] = pd.to_numeric(summary['crit_PDR_mean'], errors='coerce')
summary['crit_delay_mean_ms'] = pd.to_numeric(summary['crit_delay_mean_ms'], errors='coerce')
summary['crit_delay_max_ms'] = pd.to_numeric(summary['crit_delay_max_ms'], errors='coerce')
summary = summary.sort_values('BG', ascending=True)

fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

axes[0].plot(summary['BG'], summary['crit_PDR_mean'], marker='o', color='#1f77b4', linewidth=2)
axes[0].set_title('Experiment 3: Critical Traffic PDR vs Background Interval')
axes[0].set_xlabel('Background interval BG (s)')
axes[0].set_ylabel('Critical PDR')
axes[0].set_ylim(0.95, 1.05)
axes[0].grid(True, linestyle='--', alpha=0.35)

axes[1].plot(summary['BG'], summary['crit_delay_max_ms'], marker='s', color='#d62728', linewidth=2)
axes[1].set_title('Experiment 3: Critical Max Delay vs Background Interval')
axes[1].set_xlabel('Background interval BG (s)')
axes[1].set_ylabel('Max delay (ms)')
axes[1].grid(True, linestyle='--', alpha=0.35)

plt.tight_layout()
plt.savefig('results/exp3_visualization.png', dpi=300)
print('Saved visualization to results/exp3_visualization.png')
