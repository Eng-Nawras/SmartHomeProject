import pandas as pd

def load_and_prep(csv_path, itervar_name='I'):
    df = pd.read_csv(csv_path, low_memory=False)
    scalars = df[df['type'] == 'scalar'].copy()
    itervars = df[(df['type'] == 'itervar') & (df['attrname'] == itervar_name)][['run', 'attrvalue']]
    itervars = itervars.rename(columns={'attrvalue': 'I'})
    scalars = scalars.merge(itervars, on='run', how='left')
    scalars['I'] = scalars['I'].astype(str).str.replace('s', '', regex=False)
    scalars['I'] = pd.to_numeric(scalars['I'], errors='coerce')
    return df, scalars

# ---------------- Strategy A: Request/Response ----------------
df_rr, sc_rr = load_and_prep('results/exp4_rr_results.csv')

sent_rr = sc_rr[sc_rr['module'].str.match(r'SmartHomeNetwork\.monitoringApp\.app\[\d+\]$', na=False) &
                 (sc_rr['name'] == 'packetSent:count')].copy()
sent_rr['value'] = pd.to_numeric(sent_rr['value'], errors='coerce')
sent_per_run_rr = sent_rr.groupby('run')['value'].sum().rename('total_sent')

recv_rr = sc_rr[sc_rr['module'].str.match(r'SmartHomeNetwork\.monitoringApp\.app\[\d+\]$', na=False) &
                 (sc_rr['name'] == 'packetReceived:count')].copy()
recv_rr['value'] = pd.to_numeric(recv_rr['value'], errors='coerce')
recv_per_run_rr = recv_rr.groupby('run')['value'].sum().rename('replies_received')

run_i_rr = sc_rr.groupby('run')['I'].first()
summary_rr = pd.concat([run_i_rr, sent_per_run_rr, recv_per_run_rr], axis=1).dropna()
summary_rr['PDR'] = summary_rr['replies_received'] / summary_rr['total_sent']

# RTT: 'rcvdPkLifetime:stats' on the request-sending app (round trip: request + reply)
delay_rr = df_rr[(df_rr['type'] == 'statistic') &
                  df_rr['module'].str.match(r'SmartHomeNetwork\.monitoringApp\.app\[\d+\]$', na=False) &
                  (df_rr['name'] == 'rcvdPkLifetime:stats')].copy()
delay_rr['mean'] = pd.to_numeric(delay_rr['mean'], errors='coerce')
delay_per_run_rr = delay_rr.groupby('run')['mean'].mean().rename('mean_rtt_s')
summary_rr = summary_rr.join(delay_per_run_rr)

final_rr = summary_rr.groupby('I').agg(
    PDR_mean=('PDR', 'mean'),
    latency_mean_ms=('mean_rtt_s', lambda x: x.mean()*1000),
    total_packets_per_run=('total_sent', lambda x: x.mean()*2),  # request + reply
).reset_index().sort_values('I')
final_rr['strategy'] = 'Request/Response (RTT)'

# ---------------- Strategy B: Publish/Subscribe ----------------
df_ps, sc_ps = load_and_prep('results/exp4_ps_results.csv')

sent_ps = sc_ps[sc_ps['module'].str.match(r'SmartHomeNetwork\.(temp|motion)\d+\.app\[0\]$', na=False) &
                 (sc_ps['name'] == 'packetSent:count')].copy()
sent_ps['value'] = pd.to_numeric(sent_ps['value'], errors='coerce')
sent_per_run_ps = sent_ps.groupby('run')['value'].sum().rename('total_sent')

recv_ps = sc_ps[(sc_ps['module'] == 'SmartHomeNetwork.monitoringApp.app[0]') &
                 (sc_ps['name'] == 'packetReceived:count')].copy()
recv_ps['value'] = pd.to_numeric(recv_ps['value'], errors='coerce')
recv_per_run_ps = recv_ps.groupby('run')['value'].sum().rename('publishes_received')

run_i_ps = sc_ps.groupby('run')['I'].first()
summary_ps = pd.concat([run_i_ps, sent_per_run_ps, recv_per_run_ps], axis=1).dropna()
summary_ps['PDR'] = summary_ps['publishes_received'] / summary_ps['total_sent']

delay_ps = df_ps[(df_ps['type'] == 'histogram') &
                  (df_ps['module'] == 'SmartHomeNetwork.monitoringApp.app[0]') &
                  (df_ps['name'] == 'endToEndDelay:histogram')].copy()
delay_ps['mean'] = pd.to_numeric(delay_ps['mean'], errors='coerce')
delay_per_run_ps = delay_ps.groupby('run')['mean'].mean().rename('mean_delay_s')
summary_ps = summary_ps.join(delay_per_run_ps)

final_ps = summary_ps.groupby('I').agg(
    PDR_mean=('PDR', 'mean'),
    latency_mean_ms=('mean_delay_s', lambda x: x.mean()*1000),
    total_packets_per_run=('total_sent', 'mean'),  # publish only, one-way
).reset_index().sort_values('I')
final_ps['strategy'] = 'Publish/Subscribe (one-way)'

pd.set_option('display.width', 120)
print("=== Strategy A: Request/Response (latency = full round-trip time) ===")
print(final_rr.to_string(index=False))
print("\n=== Strategy B: Publish/Subscribe (latency = one-way delay) ===")
print(final_ps.to_string(index=False))

combined = pd.concat([final_rr, final_ps], ignore_index=True)
combined.to_csv('results/exp4_comparison.csv', index=False)
print("\nSaved comparison to results/exp4_comparison.csv")
