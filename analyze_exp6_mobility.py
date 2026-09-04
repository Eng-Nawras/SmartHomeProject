import pandas as pd

df = pd.read_csv('results/exp6_mobility_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'speed')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'speed'})
scalars = scalars.merge(itervars, on='run', how='left')
scalars['speed'] = scalars['speed'].astype(str).str.replace('mps', '', regex=False)
scalars['speed'] = pd.to_numeric(scalars['speed'], errors='coerce')

# App-layer packets sent by the mobile wearable device
sent = scalars[(scalars['module'] == 'MobilityNetwork.wearable1.app[0]') &
               (scalars['name'] == 'packetSent:count')].copy()
sent['value'] = pd.to_numeric(sent['value'], errors='coerce')
sent_per_run = sent.groupby('run')['value'].sum().rename('app_sent')

# Packets from wearable1 received at the monitoring app is not separable from
# other sensors on the shared sink port, so instead we measure PDR indirectly
# via the wearable's own MAC-layer send/ack statistics:
mac_tx = scalars[(scalars['module'] == 'MobilityNetwork.wearable1.wlan[0].mac') &
                  (scalars['name'] == 'nbTxFrames')].copy()
mac_tx['value'] = pd.to_numeric(mac_tx['value'], errors='coerce')
mac_tx_per_run = mac_tx.groupby('run')['value'].sum().rename('mac_frames_tx')

# Successfully acknowledged frames (approximates delivered frames on a single-hop link)
mac_acked = scalars[(scalars['module'] == 'MobilityNetwork.wearable1.wlan[0].mac') &
                     (scalars['name'] == 'nbRecvdAcks')].copy()
mac_acked['value'] = pd.to_numeric(mac_acked['value'], errors='coerce')
mac_acked_per_run = mac_acked.groupby('run')['value'].sum().rename('mac_frames_acked')

energy = scalars[(scalars['module'] == 'MobilityNetwork.wearable1.energyStorage') &
                  (scalars['name'] == 'residualEnergyCapacity:last')].copy()
energy['value'] = pd.to_numeric(energy['value'], errors='coerce')
energy_per_run = energy.groupby('run')['value'].apply(lambda x: -x.sum()).rename('energy_J')

run_speed = scalars.groupby('run')['speed'].first()
summary = pd.concat([run_speed, sent_per_run, mac_tx_per_run, mac_acked_per_run, energy_per_run], axis=1).dropna(subset=['speed'])
summary['link_PDR'] = summary['mac_frames_acked'] / summary['mac_frames_tx']
summary['energy_per_packet_mJ'] = (summary['energy_J'] / summary['app_sent']) * 1000

delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'MobilityNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')
summary = summary.join(delay_per_run)

final = summary.groupby('speed').agg(
    link_PDR_mean=('link_PDR', 'mean'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean() * 1000),
    mac_frames_tx=('mac_frames_tx', 'mean'),
    energy_per_packet_mJ=('energy_per_packet_mJ', 'mean'),
    n_runs=('link_PDR', 'count'),
).reset_index().sort_values('speed')

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp6_mobility_summary.csv', index=False)
print("\nSaved to results/exp6_mobility_summary.csv")
