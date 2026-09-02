import pandas as pd

df = pd.read_csv('results/exp1_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

# N per run
itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'N')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'N'})
scalars = scalars.merge(itervars, on='run', how='left')
scalars['N'] = pd.to_numeric(scalars['N'], errors='coerce')

# Received at monitoringApp application layer
received = scalars[(scalars['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                    (scalars['name'] == 'packetReceived:count')].copy()
received['value'] = pd.to_numeric(received['value'], errors='coerce')
recv_per_run = received.groupby('run')['value'].sum().rename('received')

# Sent: application layer only, avoids double-count with the .udp layer
sent = scalars[scalars['module'].str.match(r'ScalabilityNetwork\.node\[\d+\]\.app\[0\]$', na=False) &
               (scalars['name'] == 'packetSent:count')].copy()
sent['value'] = pd.to_numeric(sent['value'], errors='coerce')
sent_per_run = sent.groupby('run')['value'].sum().rename('sent')

run_n = scalars.groupby('run')['N'].first()

summary = pd.concat([run_n, sent_per_run, recv_per_run], axis=1).dropna()
summary['PDR'] = summary['received'] / summary['sent']

# Delay: comes from 'histogram' type rows, not 'statistic'
delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'ScalabilityNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')

summary = summary.join(delay_per_run)

final = summary.groupby('N').agg(
    PDR_mean=('PDR', 'mean'),
    PDR_std=('PDR', 'std'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean() * 1000),
    delay_std_ms=('mean_delay_s', lambda x: x.std() * 1000),
    n_runs=('PDR', 'count'),
).reset_index().sort_values('N')

print(final.to_string(index=False))
final.to_csv('results/exp1_summary.csv', index=False)
print("\nSaved summary to results/exp1_summary.csv")
