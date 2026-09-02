# REPRODUCIBILITY NOTE
## Smart-Home IoT Network Design and Performance Evaluation Using OMNeT++

**Project:** ENCS5325 - Wireless Sensor Networks and Internet of Things  
**University:** Birzeit University, Summer 2026  
**Date:** September 1, 2026  

---

## 1. Software Versions & Dependencies

### Required
```
OMNeT++:          6.4.0 (with WITH_OSG=no for headless operation)
INET Framework:   4.5.4 (linked to OMNeT++)
Python:           3.12+
```

### Optional (for Qtenv GUI visualization)
```
Qt5:              5.x or later
OpenGL:           2.1+
X11:              For WSL/remote environments
```

### Python Analysis Libraries
```
pandas>=1.5.0
matplotlib>=3.5.0
numpy>=1.21.0
scipy>=1.8.0
```

---

## 2. Environment Setup (One-Time)

### Linux / WSL

```bash
# Navigate to workspace
cd /home/nawras/omnetpp-workspace

# Source OMNeT++ environment
source omnetpp-6.4.0/setenv

# Verify environment variables
echo $OMNETPP_ROOT        # Should print: /home/nawras/omnetpp-workspace/omnetpp-6.4.0
echo $PATH               # Should include OMNETPP_ROOT/bin
```

### INET Framework Linking

```bash
# Verify INET is built and located at:
export INET_ROOT=/home/nawras/omnetpp-workspace/inet-4.5.4/src
ls $INET_ROOT/INET       # Should exist
```

### Python Virtual Environment

```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install pandas matplotlib numpy scipy
```

---

## 3. Exact Run Commands

### Single Experiment Run

#### Experiment 1: Scalability (N = 5, 10, 20, 30, 40)
```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject
source omnetpp-6.4.0/setenv  # or source omnetpp-6.4.0/setenv from parent

opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment1_scalability.ini -c Exp1_Scalability
```

#### Experiment 2: Reporting Interval (T = 1s, 5s, 10s, 30s, 60s)
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment2_interval.ini -c Exp2_Interval
```

#### Experiment 3: Critical Event (BG = 10s, 5s, 2s, 1s, 0.5s)
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment3_criticalevent.ini -c Exp3_CriticalEvent
```

#### Experiment 4A: Publish/Subscribe (I = 1s, 5s, 10s, 30s)
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment4_pubsub.ini -c Exp4_PubSub
```

#### Experiment 4B: Request/Response (I = 1s, 5s, 10s, 30s)
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment4_requestresponse.ini -c Exp4_RequestResponse
```

#### Experiment 5: Packet Size (L = 20B, 50B, 100B, 200B, 400B)
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment5_packetsize.ini -c Exp5_PacketSize
```

### Batch Run Script

Create `run_all_experiments.sh`:
```bash
#!/bin/bash
set -e

OMNETPP_ROOT=/home/nawras/omnetpp-workspace/omnetpp-6.4.0
INET_ROOT=/home/nawras/omnetpp-workspace/inet-4.5.4/src
PROJECT_DIR=/home/nawras/omnetpp-workspace/SmartHomeProject

# Source environment
source $OMNETPP_ROOT/setenv

cd $PROJECT_DIR

# Run all experiments
echo "Running Experiment 1: Scalability..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment1_scalability.ini -c Exp1_Scalability

echo "Running Experiment 2: Reporting Interval..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment2_interval.ini -c Exp2_Interval

echo "Running Experiment 3: Critical Event..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment3_criticalevent.ini -c Exp3_CriticalEvent

echo "Running Experiment 4A: Publish/Subscribe..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment4_pubsub.ini -c Exp4_PubSub

echo "Running Experiment 4B: Request/Response..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment4_requestresponse.ini -c Exp4_RequestResponse

echo "Running Experiment 5: Packet Size..."
opp_run -u Cmdenv -n .:"$INET_ROOT" -l "$INET_ROOT"/INET \
  experiment5_packetsize.ini -c Exp5_PacketSize

echo "All experiments completed. Results in ./results/"
```

**Run it:**
```bash
chmod +x run_all_experiments.sh
./run_all_experiments.sh
```

---

## 4. Results Processing (Python)

### Activate Virtual Environment
```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject
source .venv/bin/activate
```

### Run Analysis Scripts
```bash
# Each script reads *.sca/*.vec files from results/ and produces CSV + PNG
python analyze_exp1.py       # → exp1_results.csv, exp1_summary.csv
python analyze_exp2.py       # → exp2_results.csv, exp2_summary.csv
python analyze_exp3.py       # → exp3_results.csv, exp3_summary.csv
python analyze_exp4.py       # → exp4_ps_results.csv, exp4_rr_results.csv, exp4_comparison.csv
python analyze_exp5.py       # → exp5_results.csv, exp5_summary.csv

# Generate plots
python plot_exp1.py          # → exp1_visualization.png
python plot_exp2.py          # → exp2_visualization.png
python plot_exp3.py          # → exp3_visualization.png
python plot_exp4.py          # → exp4_visualization.png
python plot_exp5.py          # → exp5_visualization.png
```

---

## 5. Output Locations

### Simulation Results
```
results/
├── Exp1_Scalability-N=5-#0.sca
├── Exp1_Scalability-N=5-#0.vec
├── Exp1_Scalability-N=10-#0.sca
├── ...
├── Exp5_PacketSize-L=400B-#4.vec
```

### Processed Results
```
results/
├── exp1_results.csv              # Full Exp 1 data
├── exp1_summary.csv              # Exp 1 aggregated (mean ± std)
├── exp2_results.csv
├── exp2_summary.csv
├── exp3_results.csv
├── exp3_summary.csv
├── exp4_ps_results.csv           # Exp 4 Pub/Sub
├── exp4_rr_results.csv           # Exp 4 Request/Response
├── exp4_comparison.csv           # Side-by-side comparison
├── exp5_results.csv
└── exp5_summary.csv
```

### Visualizations
```
results/
├── exp1_visualization.png        # Scalability: N vs PDR, delay, throughput
├── exp2_visualization.png        # Interval: T vs delay, PDR
├── exp3_visualization.png        # Critical Event: BG load vs event latency
├── exp4_visualization.png        # Pub/Sub vs Request/Response comparison
└── exp5_visualization.png        # Packet Size vs fragmentation, delay
```

---

## 6. Key Parameters (Documented in .ini Files)

### Random Seeds
- **Seed Set:** `${repetition}` (0–4 for 5 independent runs per parameter)
- **OMNeT++ uses:** `seed-set = ${repetition}` in each config

### Simulation Time Limits
| Exp | Duration |
|-----|----------|
| 1   | 120 s    |
| 2   | 600 s    |
| 3   | 300 s    |
| 4   | 300 s    |
| 5   | 120 s    |

### Network Parameters
- **Background Noise:** –110 dBm
- **Gateway:** Bridges IEEE 802.15.4 to Ethernet
- **Routing:** Global ARP + static routes (computed at startup)

---

## 7. Notes for Reproducibility

1. **Path Consistency:** All paths are absolute. Update `/home/nawras/omnetpp-workspace/` to your installation directory if different.

2. **Execution Time:** Simulations are compute-intensive:
   - Exp 1: ~30–60 minutes (all 5 N values, 5 seeds each)
   - Exp 2: ~60–90 minutes (all 5 T values, 5 seeds each)
   - Exp 3: ~30–45 minutes (all 5 BG levels, 5 seeds each)
   - Exp 4: ~60–90 minutes (both strategies, all I values, 5 seeds each)
   - Exp 5: ~30–45 minutes (all 5 L values, 5 seeds each)
   - **Total:** ~4–6 hours

3. **Output Files:** Results accumulate in `results/`. Ensure sufficient disk space (~500 MB–1 GB for all experiments).

4. **Seed Reproducibility:** Results are deterministic within a single OMNeT++ version. Different OMNeT++ versions may produce slightly different numeric results due to RNG implementation differences.

5. **GUI Visualization (Optional):**
   - To view real-time topology in Qtenv, use X11 forwarding (Linux/native systems only).
   - WSL users: Install VcXsrv and set `export DISPLAY=:0`, then replace `-u Cmdenv` with `-u Qtenv`.

---

## 8. Verification Checklist

- [ ] OMNeT++ version 6.4.0 installed and `setenv` sourced.
- [ ] INET 4.5.4 built and `INET_ROOT` set.
- [ ] Python 3.12+ with pandas, matplotlib, numpy installed.
- [ ] `experiment*.ini` files present in project root.
- [ ] `SmartHomeNetwork.ned` and `ScalabilityNetwork.ned` present.
- [ ] `results/` directory exists and is writable.
- [ ] Sample run (Exp 1, N=5, seed #0) completes without errors.
- [ ] CSV and PNG files are generated after analysis script runs.

---

## 9. Contact Information

For questions or issues with reproducibility:
- **Supervisor:** [To be updated]
- **Project Team:** [Student names — to be updated]

---

**Document Version:** 1.0  
**Last Updated:** September 1, 2026  
**Status:** Ready for submission
