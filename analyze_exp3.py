import pandas as pd

df = pd.read_csv('results/exp3_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

itervars = df[(df['type'] == 'itervar') & (df['attrname'] == 'BG')][['run', 'attrvalue']]
itervars = itervars.rename(columns={'attrvalue': 'BG'})
scalars = scalars.merge(itervars, on='run', how='left')
scalars['BG'] = scalars['BG'].astype(str).str.replace('s', '', regex=False)
scalars['BG'] = pd.to_numeric(scalars['BG'], errors='coerce')

# Critical (smoke) traffic received at monitoringApp.app[1] (port 5001, dedicated sink)
recv_crit = scalars[(scalars['module'] == 'SmartHomeNetwork.monitoringApp.app[1]') &
                     (scalars['name'] == 'packetReceived:count')].copy()
recv_crit['value'] = pd.to_numeric(recv_crit['value'], errors='coerce')
recv_crit_per_run = recv_crit.groupby('run')['value'].sum().rename('crit_received')

sent_crit = scalars[scalars['module'].str.match(r'SmartHomeNetwork\.smoke\d+\.app\[0\]$', na=False) &
                     (scalars['name'] == 'packetSent:count')].copy()
sent_crit['value'] = pd.to_numeric(sent_crit['value'], errors='coerce')
sent_crit_per_run = sent_crit.groupby('run')['value'].sum().rename('crit_sent')

run_bg = scalars.groupby('run')['BG'].first()

summary = pd.concat([run_bg, sent_crit_per_run, recv_crit_per_run], axis=1).dropna()
summary['crit_PDR'] = summary['crit_received'] / summary['crit_sent']
summary['crit_loss'] = 1 - summary['crit_PDR']

# Critical event delay: histogram stats for monitoringApp.app[1] only (smoke traffic port)
delay_crit = df[(df['type'] == 'histogram') &
                (df['module'] == 'SmartHomeNetwork.monitoringApp.app[1]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
for col in ['mean', 'max', 'stddev']:
    delay_crit[col] = pd.to_numeric(delay_crit[col], errors='coerce')
delay_summary = delay_crit.groupby('run').agg(mean_delay_s=('mean','mean'),
                                                max_delay_s=('max','max'),
                                                jitter_s=('stddev','mean'))
summary = summary.join(delay_summary)

final = summary.groupby('BG').agg(
    crit_PDR_mean=('crit_PDR', 'mean'),
    crit_loss_mean=('crit_loss', 'mean'),
    crit_delay_mean_ms=('mean_delay_s', lambda x: x.mean()*1000),
    crit_delay_max_ms=('max_delay_s', lambda x: x.max()*1000),
    jitter_ms=('jitter_s', lambda x: x.mean()*1000),
    n_runs=('crit_PDR', 'count'),
).reset_index().sort_values('BG', ascending=False)  # BG=10s (light) -> 0.5s (heavy)

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp3_summary.csv', index=False)

# Latency requirement check: assume 100 ms is a reasonable smoke-alarm requirement
LATENCY_REQ_MS = 100
final['meets_100ms_requirement'] = final['crit_delay_max_ms'] < LATENCY_REQ_MS
print(f"\nLatency requirement check (max delay < {LATENCY_REQ_MS} ms):")
print(final[['BG', 'crit_delay_max_ms', 'meets_100ms_requirement']].to_string(index=False))
print("\nSaved to results/exp3_summary.csv")
