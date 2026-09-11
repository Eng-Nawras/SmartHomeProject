import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/exp9_wifi_coexistence_summary.csv")

plt.figure(figsize=(8, 5))
plt.errorbar(
    df["config"],
    df["smart_home_received_mean"],
    yerr=df["smart_home_received_std"],
    marker="o",
    capsize=5
)

plt.xlabel("Wi-Fi Load")
plt.ylabel("Smart Home Packets Received")
plt.title("Impact of Wi-Fi Coexistence on Smart Home Traffic")
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "results/exp9_wifi_coexistence.png",
    dpi=300,
    bbox_inches="tight"
)

print("Saved to results/exp9_wifi_coexistence.png")
