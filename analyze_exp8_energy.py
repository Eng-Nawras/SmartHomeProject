import pandas as pd

df = pd.read_csv('results/exp8_energy_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

SIM_TIME_S = 60.0
FRAME_AIRTIME_S = 0.00246       # ~2.46 ms/frame @ 250 kbps, 77B frame (matches Section 6 fragmentation analysis)
TX_POWER_MW = 52.2              # CC2420 datasheet, 0 dBm TX
RX_POWER_MW = 59.1              # CC2420 datasheet, RX
IDLE_POWER_MW = 1.28            # CC2420 datasheet, idle/CCA listen

NODES = ['temp1', 'smoke1', 'gateway', 'motion1', 'hvac1']

rows = []
for node in NODES:
    mac = f'SmartHomeNetwork.{node}.wlan[0].mac'
    tx = scalars[(scalars['module'] == mac) & (scalars['name'] == 'nbTxFrames')].copy()
    rx = scalars[(scalars['module'] == mac) & (scalars['name'] == 'nbRxFrames')].copy()
    tx['value'] = pd.to_numeric(tx['value'], errors='coerce')
    rx['value'] = pd.to_numeric(rx['value'], errors='coerce')
    tx_by_run = tx.groupby('run')['value'].sum()
    rx_by_run = rx.groupby('run')['value'].sum()

    energy = scalars[(scalars['module'] == f'SmartHomeNetwork.{node}.energyStorage') &
                      (scalars['name'] == 'residualEnergyCapacity:last')].copy()
    energy['value'] = pd.to_numeric(energy['value'], errors='coerce')
    measured_total_mJ_by_run = energy.groupby('run')['value'].sum().apply(lambda x: -x * 1000)

    for run in tx_by_run.index:
        n_tx = tx_by_run.get(run, 0)
        n_rx = rx_by_run.get(run, 0)
        tx_time = n_tx * FRAME_AIRTIME_S
        rx_time = n_rx * FRAME_AIRTIME_S
        idle_time = max(0, SIM_TIME_S - tx_time - rx_time)
        tx_energy = tx_time * TX_POWER_MW
        rx_energy = rx_time * RX_POWER_MW
        idle_energy = idle_time * IDLE_POWER_MW
        rows.append({
            'node': node, 'run': run,
            'tx_energy_mJ': tx_energy, 'rx_energy_mJ': rx_energy, 'idle_energy_mJ': idle_energy,
            'analytical_total_mJ': tx_energy + rx_energy + idle_energy,
            'measured_total_mJ': measured_total_mJ_by_run.get(run, float('nan')),
        })

result = pd.DataFrame(rows)
summary = result.groupby('node').mean(numeric_only=True).drop(columns=['run'], errors='ignore').reset_index()
summary['match_pct'] = 100 * summary['analytical_total_mJ'] / summary['measured_total_mJ']

pd.set_option('display.width', 140)
print(summary.round(4).to_string(index=False))
summary.to_csv('results/exp8_energy_summary.csv', index=False)
print("\nSaved to results/exp8_energy_summary.csv")
