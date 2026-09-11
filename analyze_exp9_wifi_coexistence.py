import glob
import os
import re
import statistics
import csv

RESULT_DIR = "results"
configs = ["NoWiFi", "Low", "Medium", "High"]

rows = []

for config in configs:
    files = sorted(glob.glob(f"{RESULT_DIR}/Exp9_{config}-#*.sca"))

    received = []
    wifi_sent = []
    wifi_received = []

    for f in files:
        text = open(f, encoding="utf-8", errors="ignore").read()

        m = re.search(
            r"monitoringApp\.udp packetReceived:count\s+([0-9.eE+-]+)",
            text
        )
        if m:
            received.append(float(m.group(1)))

        m = re.search(
            r"wifiHost1\.udp packetSent:count\s+([0-9.eE+-]+)",
            text
        )
        if m:
            wifi_sent.append(float(m.group(1)))

        m = re.search(
            r"wifiHost2\.udp packetReceived:count\s+([0-9.eE+-]+)",
            text
        )
        if m:
            wifi_received.append(float(m.group(1)))

    if received:
        rows.append({
            "config": config,
            "n_runs": len(received),
            "smart_home_received_mean": statistics.mean(received),
            "smart_home_received_std": statistics.stdev(received) if len(received) > 1 else 0,
            "wifi_sent_mean": statistics.mean(wifi_sent) if wifi_sent else 0,
            "wifi_received_mean": statistics.mean(wifi_received) if wifi_received else 0,
        })

out = f"{RESULT_DIR}/exp9_wifi_coexistence_summary.csv"

with open(out, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("\nExp9 Wi-Fi Coexistence Summary")
print("=" * 80)

for r in rows:
    print(
        f"{r['config']:8s} | "
        f"SmartHome RX = {r['smart_home_received_mean']:.2f} "
        f"+/- {r['smart_home_received_std']:.2f} | "
        f"WiFi TX = {r['wifi_sent_mean']:.0f} | "
        f"WiFi RX = {r['wifi_received_mean']:.0f} | "
        f"runs = {r['n_runs']}"
    )

print(f"\nSaved to {out}")
