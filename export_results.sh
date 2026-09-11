#!/usr/bin/env bash
# Export local OMNeT++ scalar/vector files to the CSV-R inputs consumed by
# the analysis scripts. Run this after simulations and before plotting.
set -euo pipefail

OMNETPP_ROOT="${OMNETPP_ROOT:-/home/nawras/omnetpp-workspace/omnetpp-6.4.0}"
source "$OMNETPP_ROOT/setenv" >/dev/null

export_one() {
    local output="$1"
    local pattern="$2"
    opp_scavetool export -F CSV-R -o "results/$output" "results/$pattern"
}

export_one exp1_results.csv 'Exp1_Scalability-*.sca'
export_one exp1_stress_results.csv 'Exp1_Stress-*.sca'
export_one exp2_results.csv 'Exp2_Interval-*.sca'
export_one exp3_results.csv 'Exp3_CriticalEvent-*.sca'
export_one exp4_ps_results.csv 'Exp4_PubSub-*.sca'
export_one exp4_rr_results.csv 'Exp4_RequestResponse-*.sca'
export_one exp5_results.csv 'Exp5_PacketSize-*.sca'
export_one exp6_mobility_results.csv 'Exp6_Mobility-*.sca'
export_one exp7_obstacles_results.csv 'Exp7_*.sca'
# Experiment 8 reads sample-and-hold values from the native .vec files;
# CSV-R exports vector metadata but not the samples needed for integration.

python3 analyze_exp1.py
python3 analyze_exp1_full.py
python3 analyze_exp1_stress.py
python3 analyze_exp2.py
python3 analyze_exp3.py
python3 analyze_exp4.py
python3 analyze_exp5.py
python3 analyze_exp6_mobility.py
python3 analyze_exp7_obstacles.py
python3 analyze_exp8_energy.py
python3 analyze_exp9_wifi_coexistence.py

python3 plot_exp1.py
python3 plot_exp2.py
python3 plot_exp3.py
python3 plot_exp4.py
python3 plot_exp5.py
python3 plot_exp6_mobility.py
python3 plot_exp7_obstacles.py
python3 plot_exp8_energy.py
python3 plot_exp9_wifi_coexistence.py
