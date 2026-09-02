import pandas as pd

df = pd.read_csv('results/exp2_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'T')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'T'})
scalars = scalars.merge(itervars, on='run', how='left')
# T comes as e.g. "1s" -- strip the trailing 's' and convert to float seconds
scalars['T'] = scalars['T'].astype(str).str.replace('s', '', regex=False)
scalars['T'] = pd.to_numeric(scalars['T'], errors='coerce')

received = scalars[(scalars['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                    (scalars['name'] == 'packetReceived:count')].copy()
received['value'] = pd.to_numeric(received['value'], errors='coerce')
recv_per_run = received.groupby('run')['value'].sum().rename('received')

sent = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.app\[0\]$', na=False) &
               (scalars['name'] == 'packetSent:count')].copy()
sent['value'] = pd.to_numeric(sent['value'], errors='coerce')
sent_per_run = sent.groupby('run')['value'].sum().rename('sent')

energy = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.energyStorage$', na=False) &
                  (scalars['name'] == 'residualEnergyCapacity:last')].copy()
energy['value'] = pd.to_numeric(energy['value'], errors='coerce')
energy_consumed_total = energy.groupby('run')['value'].apply(lambda x: -x.sum()).rename('energy_consumed_J')

run_t = scalars.groupby('run')['T'].first()

summary = pd.concat([run_t, sent_per_run, recv_per_run, energy_consumed_total], axis=1).dropna()
summary['PDR'] = summary['received'] / summary['sent']
summary['energy_per_node_J'] = summary['energy_consumed_J'] / 12  # 12 nodes fixed

delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')
summary = summary.join(delay_per_run)

final = summary.groupby('T').agg(
    PDR_mean=('PDR', 'mean'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean() * 1000),
    energy_per_node_J=('energy_per_node_J', 'mean'),
    n_runs=('PDR', 'count'),
).reset_index().sort_values('T')

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp2_summary.csv', index=False)
print("\nSaved to results/exp2_summary.csv")
