import pandas as pd

df = pd.read_csv('results/exp5_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'L')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'L'})
scalars = scalars.merge(itervars, on='run', how='left')
scalars['L'] = scalars['L'].astype(str).str.replace('B', '', regex=False)
scalars['L'] = pd.to_numeric(scalars['L'], errors='coerce')

sent = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.app\[0\]$', na=False) &
               (scalars['name'] == 'packetSent:count')].copy()
sent['value'] = pd.to_numeric(sent['value'], errors='coerce')
sent_per_run = sent.groupby('run')['value'].sum().rename('app_sent')

recv = scalars[(scalars['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
               (scalars['name'] == 'packetReceived:count')].copy()
recv['value'] = pd.to_numeric(recv['value'], errors='coerce')
recv_per_run = recv.groupby('run')['value'].sum().rename('app_received')

# Link-layer (MAC) transmission count: nbTxFrames per node
mac_sent = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.wlan\[0\]\.mac$', na=False) &
                    (scalars['name'] == 'nbTxFrames')].copy()
mac_sent['value'] = pd.to_numeric(mac_sent['value'], errors='coerce')
mac_sent_per_run = mac_sent.groupby('run')['value'].sum().rename('mac_frames_tx')

energy = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.energyStorage$', na=False) &
                  (scalars['name'] == 'residualEnergyCapacity:last')].copy()
energy['value'] = pd.to_numeric(energy['value'], errors='coerce')
energy_per_run = energy.groupby('run')['value'].apply(lambda x: -x.sum()).rename('energy_J')

run_l = scalars.groupby('run')['L'].first()
summary = pd.concat([run_l, sent_per_run, recv_per_run, mac_sent_per_run, energy_per_run], axis=1).dropna()
summary['PDR'] = summary['app_received'] / summary['app_sent']
summary['mac_frames_per_app_pkt'] = summary['mac_frames_tx'] / summary['app_sent']
summary['energy_per_packet_mJ'] = (summary['energy_J'] / summary['app_received']) * 1000

delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')
summary = summary.join(delay_per_run)

final = summary.groupby('L').agg(
    PDR_mean=('PDR', 'mean'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean()*1000),
    mac_frames_per_app_pkt=('mac_frames_per_app_pkt', 'mean'),
    energy_per_packet_mJ=('energy_per_packet_mJ', 'mean'),
    n_runs=('PDR', 'count'),
).reset_index().sort_values('L')

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp5_summary.csv', index=False)
print("\nSaved to results/exp5_summary.csv")
