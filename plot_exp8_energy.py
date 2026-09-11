"""Plot Experiment 8 advanced energy results."""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/exp8_energy_summary.csv")

nodes = df["node"].tolist()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# ---------------------------------------------------------
# 1. Radio energy breakdown
# ---------------------------------------------------------

bottom = np.zeros(len(df))

energy_columns = [
    ("idle_or_cca_energy_mJ", "Idle/CCA"),
    ("receive_energy_mJ", "Receive"),
    ("transmit_energy_mJ", "Transmit"),
    ("switching_energy_mJ", "Switching"),
]

for column, label in energy_columns:
    axes[0].bar(
        nodes,
        df[column],
        bottom=bottom,
        label=label
    )
    bottom += df[column].to_numpy()

axes[0].set_ylabel("Energy per 60 s run (mJ)")
axes[0].set_title(
    "Experiment 8 (Bonus): Radio Energy Breakdown"
)
axes[0].legend()
axes[0].grid(True, alpha=0.3, axis="y")

plt.setp(
    axes[0].get_xticklabels(),
    rotation=30
)

# ---------------------------------------------------------
# 2. Radio energy per device
# ---------------------------------------------------------

x = np.arange(len(nodes))
width = 0.45

axes[1].bar(
    x,
    df["observed_radio_energy_mJ"],
    width,
    label="Radio energy"
)

axes[1].set_xticks(x)
axes[1].set_xticklabels(
    nodes,
    rotation=30
)

axes[1].set_ylabel(
    "Radio energy per 60 s run (mJ)"
)

axes[1].set_title(
    "Experiment 8 (Bonus): Total Radio Energy"
)

axes[1].legend()
axes[1].grid(True, alpha=0.3, axis="y")

plt.tight_layout()

output = "results/exp8_energy_breakdown.png"
plt.savefig(output, dpi=300, bbox_inches="tight")

print(f"Saved: {output}")

plt.show()
