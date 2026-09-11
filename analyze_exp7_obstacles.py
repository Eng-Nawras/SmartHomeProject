import pandas as pd
import re

df = pd.read_csv('results/exp7_obstacles_results.csv', low_memory=False)
scalars = df[df['type'] == 'scalar'].copy()

# Config name (Exp7_NoWalls / Exp7_WithWalls) is the first token of the run id
scalars['config'] = scalars['run'].str.split('-').str[0]

OBSTRUCTED = ['temp1', 'smoke1', 'smoke2']       # behind the wall
UNOBSTRUCTED = ['temp2', 'temp3', 'motion1', 'motion2', 'motion3']  # open line of sight

def link_pdr_for_group(nodes):
    pattern = r'^WallsNetwork\.(' + '|'.join(nodes) + r')\.wlan\[0\]\.mac$'
    tx = scalars[scalars['module'].str.match(pattern, na=False) & (scalars['name'] == 'nbTxFrames')].copy()
    tx['value'] = pd.to_numeric(tx['value'], errors='coerce')
    tx_per_run = tx.groupby('run')['value'].sum().rename('tx')

    ack = scalars[scalars['module'].str.match(pattern, na=False) & (scalars['name'] == 'nbRecvdAcks')].copy()
    ack['value'] = pd.to_numeric(ack['value'], errors='coerce')
    ack_per_run = ack.groupby('run')['value'].sum().rename('ack')

    g = pd.concat([tx_per_run, ack_per_run], axis=1).dropna()
    g['link_PDR'] = g['ack'] / g['tx']
    return g

obstructed = link_pdr_for_group(OBSTRUCTED)
unobstructed = link_pdr_for_group(UNOBSTRUCTED)

run_config = scalars.groupby('run')['config'].first()

delay_rows = df[(df['type'] == 'histogram') &
                (df['module'] == 'WallsNetwork.monitoringApp.app[0]') &
                (df['name'] == 'endToEndDelay:histogram')].copy()
delay_rows['mean'] = pd.to_numeric(delay_rows['mean'], errors='coerce')
delay_per_run = delay_rows.groupby('run')['mean'].mean().rename('mean_delay_s')

summary = pd.DataFrame({
    'config': run_config,
    'obstructed_link_PDR': obstructed['link_PDR'],
    'unobstructed_link_PDR': unobstructed['link_PDR'],
}).join(delay_per_run).dropna(subset=['config'])

final = summary.groupby('config').agg(
    obstructed_PDR_mean=('obstructed_link_PDR', 'mean'),
    unobstructed_PDR_mean=('unobstructed_link_PDR', 'mean'),
    delay_mean_ms=('mean_delay_s', lambda x: x.mean() * 1000),
    n_runs=('obstructed_link_PDR', 'count'),
).reset_index()

pd.set_option('display.width', 120)
print(final.to_string(index=False))
final.to_csv('results/exp7_obstacles_summary.csv', index=False)
print("\nSaved to results/exp7_obstacles_summary.csv")
