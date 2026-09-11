import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results/exp7_obstacles_summary.csv').set_index('config')

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

configs = df.index.tolist()
x = np.arange(len(configs))
width = 0.35

axes[0].bar(x - width/2, df['obstructed_PDR_mean'], width, label='Obstructed (behind wall)', color='tab:red')
axes[0].bar(x + width/2, df['unobstructed_PDR_mean'], width, label='Unobstructed (open LOS)', color='tab:green')
axes[0].set_xticks(x)
axes[0].set_xticklabels(configs)
axes[0].set_ylabel('Link PDR')
axes[0].set_title('Experiment 7 (Bonus): Link PDR by Group')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

axes[1].bar(configs, df['delay_mean_ms'], color='tab:orange')
axes[1].set_ylabel('Delay (ms)')
axes[1].set_title('Experiment 7 (Bonus): Network Mean Delay')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('results/exp7_obstacles_visualization.png', dpi=300)
print("Saved results/exp7_obstacles_visualization.png")
