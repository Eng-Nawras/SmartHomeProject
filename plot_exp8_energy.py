import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('results/exp8_energy_summary.csv')
nodes = df['node'].tolist()

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# --- Stacked bar: analytical energy breakdown (mJ) per node ---
axes[0].bar(nodes, df['idle_energy_mJ'], label='Idle/CCA', color='#55a868')
axes[0].bar(nodes, df['rx_energy_mJ'], bottom=df['idle_energy_mJ'], label='Receive', color='#4c72b0')
axes[0].bar(nodes, df['tx_energy_mJ'], bottom=df['idle_energy_mJ'] + df['rx_energy_mJ'], label='Transmit', color='#c44e52')
axes[0].set_ylabel('Energy per 60s run (mJ)')
axes[0].set_title('Experiment 8 (Bonus): Analytical Energy Breakdown')
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis='y')
plt.setp(axes[0].get_xticklabels(), rotation=20)

# --- Validation: analytical vs measured total energy ---
x = np.arange(len(nodes))
width = 0.35
axes[1].bar(x - width/2, df['analytical_total_mJ'], width, label='Analytical (breakdown)', color='#8172b2')
axes[1].bar(x + width/2, df['measured_total_mJ'], width, label='Measured (simulation)', color='#ccb974')
axes[1].set_xticks(x)
axes[1].set_xticklabels(nodes, rotation=20)
axes[1].set_ylabel('Total energy per 60s run (mJ)')
axes[1].set_title('Experiment 8 (Bonus): Analytical vs Measured Validation')
axes[1].legend()
axes[1].grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('results/exp8_energy_visualization.png', dpi=300)
print("Saved results/exp8_energy_visualization.png")
