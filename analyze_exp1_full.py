import pandas as pd

df = pd.read_csv('results/exp1_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'N')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'N'})
scalars = scalars.merge(itervars, on='run', how='left')
scalars['N'] = pd.to_numeric(scalars['N'], errors='coerce')

received = scalars[(scalars['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                    (scalars['name'] == 'packetReceived:count')].copy()
received['value'] = pd.to_numeric(received['value'], errors='coerce')
recv_per_run = received.groupby('run')['value'].sum().rename('received')

recv_bytes = scalars[(scalars['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                      (scalars['name'] == 'packetReceived:sum(packetBytes)')].copy()
recv_bytes['value'] = pd.to_numeric(recv_bytes['value'], errors='coerce')
recv_bytes_per_run = recv_bytes.groupby('run')['value'].sum().rename('received_bytes')

sent = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.app\[0\]$', na=False) &
               (scalars['name'] == 'packetSent:count')].copy()
sent['value'] = pd.to_numeric(sent['value'], errors='coerce')
sent_per_run = sent.groupby('run')['value'].sum().rename('sent')

energy = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.energyStorage$', na=False) &
                  (scalars['name'] == 'residualEnergyCapacity:last')].copy()
energy['value'] = pd.to_numeric(energy['value'], errors='coerce')
energy_consumed_total = energy.groupby('run')['value'].apply(lambda x: -x.sum()).rename('energy_consumed_J')

run_n = scalars.groupby('run')['N'].first()

summary = pd.concat([run_n, sent_per_run, recv_per_run, recv_bytes_per_run, energy_consumed_total], axis=1).dropna()
summary['PDR'] = summary['received'] / summary['sent']
summary['loss_ratio'] = 1 - summary['PDR']
summary['throughput_bps'] = (summary['received_bytes'] * 8) / 120.0
summary['energy_per_packet_mJ'] = (summary['energy_consumed_J'] / summary['received']) * 1000

delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')
summary = summary.join(delay_per_run)

final = summary.groupby('N').agg(
    PDR_mean=('PDR', 'mean'),
    loss_mean=('loss_ratio', 'mean'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean() * 1000),
    throughput_mean_bps=('throughput_bps', 'mean'),
    energy_per_packet_mJ=('energy_per_packet_mJ', 'mean'),
    n_runs=('PDR', 'count'),
).reset_index().sort_values('N')

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp1_summary_full.csv', index=False)
print("\nSaved to results/exp1_summary_full.csv")
