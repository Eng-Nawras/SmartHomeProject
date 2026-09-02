# Smart-Home IoT Network Design and Performance Evaluation Using OMNeT++

**Course:** ENCS5325 - Wireless Sensor Networks and Internet of Things  
**University:** Birzeit University, Summer 2026  
**Project Date:** August 22, 2026  
**Due Date:** September 12, 2026  

---

## 1. Network Topology (SmartHomeNetwork)

### Baseline Scenario: 12 Device Smart-Home Network

```
┌─────────────────────────── WIRELESS 802.15.4 SIDE ──────────────────────┐
│                                                                           │
│  Periodic Sensors:              Event-Driven Sensors:                    │
│  • temp1, temp2, temp3          • smoke1, smoke2                         │
│  • motion1, motion2, motion3                                             │
│                                 Actuators:                               │
│  ┌──────────────────────────┐   • light1, light2                         │
│  │     IEEE 802.15.4        │   • hvac1                                  │
│  │   Radio Medium (PHY)     │   • alarm1                                 │
│  └──────────────────────────┘                                            │
│            ▲                                                              │
│            │ (wireless link)                                             │
│            │                                                              │
│      ┌─────▼──────┐                                                      │
│      │   Gateway   │ (Router with IEEE 802.15.4 + Ethernet)             │
│      └─────┬──────┘                                                      │
│            │                                                              │
└────────────┼──────────────────────────────────────────────────────────────┘
             │ (Ethernet link)
             │
┌────────────┼──────────────────── WIRED CORE SIDE ────────────────────────┐
│            │                                                             │
│      ┌─────▼──────────┐         ┌──────────────────────┐                │
│      │  Core Switch   │◄───────►│  Monitoring App      │                │
│      │  (Eth1G)       │         │  (CoAP/MQTT Broker)  │                │
│      └────────────────┘         └──────────────────────┘                │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
```

### Device Configuration

| Device Type    | Device Names       | Count | Role                          |
|----------------|--------------------|-------|-------------------------------|
| **Sensors**    | temp1–3            | 3     | Temperature/Humidity (periodic) |
|                | motion1–3          | 3     | Occupancy/Motion (periodic)   |
|                | smoke1–2           | 2     | Environmental/Smoke (event)   |
| **Actuators**  | light1–2           | 2     | Controllable lights           |
|                | hvac1              | 1     | HVAC (climate control)        |
|                | alarm1             | 1     | Smart alarm/notification      |
| **Network**    | gateway            | 1     | Border router (802.15.4↔IP)   |
| **Core**       | coreSwitch         | 1     | Ethernet switch               |
|                | monitoringApp      | 1     | Application server (broker)   |
| **Total**      | -                  | **12** | -                             |

### Network Stack

```
Application Layer:  UdpBasicApp (sensors) → UdpSink (monitoring app)
Transport Layer:    UDP
Network Layer:      IPv4 + IPv6/6LoWPAN (compression for 802.15.4)
Link Layer:         IEEE 802.15.4 (narrowband)
PHY Layer:          Ieee802154NarrowbandScalarRadioMedium
```

### Baseline Parameters

| Parameter              | Value       |
|------------------------|-------------|
| Nodes (Baseline)       | 12          |
| Access Technology      | IEEE 802.15.4 |
| Baseline Payload       | 50 B        |
| Baseline Interval      | 10 s        |
| Critical Event Rate    | Exponential (15 s) |
| Simulation Duration    | 120–600 s   |
| Random Seeds           | 5 per run   |
| Background Noise Power | –110 dBm    |

---

## 2. Experiments Overview

### Experiment 1: Network Scalability
**Objective:** Determine how network load scales with node count.

| Parameter      | Values              | Runs | Seeds |
|----------------|---------------------|------|-------|
| Number of Nodes (N) | 5, 10, 20, 30, 40 | 5    | 5     |
| Payload        | 50 B (fixed)        | -    | -     |
| Interval       | 10 s (fixed)        | -    | -     |
| Sim Time       | 120 s               | -    | -     |
| **Total Runs** | **25** (5 × 5)      | -    | -     |

**Metrics:** PDR (Packet Delivery Ratio), latency, throughput, loss, energy/packet

**Topology:** ScalabilityNetwork with parametric `node[numNodes]`

---

### Experiment 2: Reporting Interval & Energy Trade-Off
**Objective:** Analyze freshness vs. energy/latency trade-off.

| Parameter      | Values              | Runs | Seeds |
|----------------|---------------------|------|-------|
| Interval (T)   | 1 s, 5 s, 10 s, 30 s, 60 s | 5 | 5 |
| Nodes          | 12 (fixed)          | -    | -     |
| Payload        | 50 B (fixed)        | -    | -     |
| Sim Time       | 600 s               | -    | -     |
| **Total Runs** | **25** (5 × 5)      | -    | -     |

**Metrics:** Delay, PDR, energy consumption, radio-active time

---

### Experiment 3: Critical Event under Background Load
**Objective:** Assess event latency and reliability under varying traffic loads.

| Parameter      | Values              | Runs | Seeds |
|----------------|---------------------|------|-------|
| Background Load (BG) | 10 s, 5 s, 2 s, 1 s, 0.5 s | 5 | 5 |
| Nodes          | 12 (fixed, SmartHomeNetwork) | - | - |
| Payload        | 50 B (fixed)        | -    | -     |
| Critical Event Rate | Exp(15 s)       | -    | -     |
| Sim Time       | 300 s               | -    | -     |
| **Total Runs** | **25** (5 × 5)      | -    | -     |

**Metrics:** Event latency, loss probability, jitter, max delay, PDR under load

**Note:** Background sensors send at variable intervals; smoke detectors send events independently.

---

### Experiment 4: Application Communication Strategy
**Objective:** Compare Publish/Subscribe vs. Request/Response patterns.

#### Strategy A: Publish/Subscribe (MQTT-like)
```
Sensors → [direct publish] → Monitoring App (broker)
```

#### Strategy B: Request/Response (CoAP-like)
```
Monitoring App → [poll request] → Sensor → [response] → Monitoring App
```

| Parameter      | Pub/Sub             | Request/Response   | Seeds |
|----------------|---------------------|--------------------|-------|
| Interval (I)   | 1 s, 5 s, 10 s, 30 s| 1 s, 5 s, 10 s, 30 s| 5 |
| Nodes          | 12 (fixed)          | 12 (fixed)         | -     |
| Payload        | 50 B                | 50 B               | -     |
| Sim Time       | 300 s               | 300 s              | -     |
| **Total Runs** | **20** (4 × 5)      | **20** (4 × 5)     | -     |

**Metrics:** Latency, throughput, PDR, traffic overhead

---

### Experiment 5: Packet Size & 6LoWPAN Fragmentation
**Objective:** Relate payload size to fragmentation and cross-layer overhead.

| Parameter      | Values              | Runs | Seeds |
|----------------|---------------------|------|-------|
| Payload Size (L) | 20 B, 50 B, 100 B, 200 B, 400 B | 5 | 5 |
| Nodes          | 12 (fixed)          | -    | -     |
| Interval       | 5 s (fixed)         | -    | -     |
| Sim Time       | 120 s               | -    | -     |
| **Total Runs** | **25** (5 × 5)      | -    | -     |

**Cross-Layer Analysis:**
- IEEE 802.15.4 frame limit: 127 octets (PSDU)
- IPv6 header: 40 octets
- UDP header: 8 octets
- 6LoWPAN compression reduces IPv6 header to ~2–6 octets
- Fragmentation threshold: ~60–80 octets (depending on header compression)

**Metrics:** Fragmentation rate, airtime, delay, PDR, retransmission exposure, energy

---

## 3. Results Summary

### Results Directory Structure

```
results/
├── Baseline-#0.{sca,vci,vec}
├── Exp1_Scalability-N={5,10,20,30,40}-#{0..4}.{sca,vci,vec}
├── Exp1_Stress-N={5,10,20,30,40}-#{0..2}.{sca,vci,vec}
├── Exp2_Interval-T={1s,5s,10s,30s,60s}-#{0..4}.{sca,vci,vec}
├── Exp3_CriticalEvent-BG={10s,5s,2s,1s,0.5s}-#{0..4}.{sca,vci,vec}
├── Exp4_PubSub-I={1s,5s,10s,30s}-#{0..4}.{sca,vci,vec}
├── Exp4_RequestResponse-I={1s,5s,10s,30s}-#{0..4}.{sca,vci,vec}
├── Exp5_PacketSize-L={20B,50B,100B,200B,400B}-#{0..4}.{sca,vci,vec}
├── exp1_results.csv
├── exp1_summary.csv
├── exp2_results.csv
├── exp2_summary.csv
├── exp3_results.csv
├── exp3_summary.csv
├── exp4_comparison.csv
├── exp4_ps_results.csv
├── exp4_rr_results.csv
├── exp5_results.csv
├── exp5_summary.csv
├── exp{1..5}_visualization.png
└── ...
```

### Result File Types

- **`.sca` (Scalar results):** Aggregated metrics (PDR, avg delay, throughput)
- **`.vec` (Vector results):** Time-series data (packet arrivals, delays over time)
- **`.csv` (Summaries):** Processed results per experiment parameter
- **`.png` (Visualizations):** Plots of key metrics vs. parameters

---

## 4. Project Files

### Core Model Files

| File                        | Purpose                                |
|-----------------------------|----------------------------------------|
| `SmartHomeNetwork.ned`      | Fixed 12-node topology (Experiments 3–4) |
| `ScalabilityNetwork.ned`    | Parametric topology (Experiments 1–2, 5) |
| `package.ned`               | Package declaration                    |

### Configuration Files

| File                            | Experiment | Parameters              |
|---------------------------------|------------|------------------------|
| `baseline.ini`                  | Baseline   | Baseline 12-node setup  |
| `experiment1_scalability.ini`   | 1          | N = 5, 10, 20, 30, 40  |
| `experiment1_stress.ini`        | 1 (stress) | Higher payload/freq    |
| `experiment2_interval.ini`      | 2          | T = 1–60 s             |
| `experiment3_criticalevent.ini` | 3          | BG = 0.5–10 s          |
| `experiment4_pubsub.ini`        | 4a         | I = 1–30 s (Pub/Sub)   |
| `experiment4_requestresponse.ini` | 4b       | I = 1–30 s (Req/Resp)  |
| `experiment5_packetsize.ini`    | 5          | L = 20–400 B           |

### Analysis Scripts

| File                    | Purpose                              |
|-------------------------|--------------------------------------|
| `analyze_exp1.py`       | Exp 1 results processing             |
| `analyze_exp1_full.py`  | Exp 1 detailed analysis              |
| `analyze_exp1_stress.py`| Exp 1 stress scenario                |
| `analyze_exp2.py`       | Exp 2 results processing             |
| `analyze_exp3.py`       | Exp 3 results processing             |
| `analyze_exp4.py`       | Exp 4 comparison (Pub/Sub vs Req/Resp) |
| `analyze_exp5.py`       | Exp 5 packet-size analysis           |
| `plot_exp{1..5}.py`     | Visualization generation             |

---

## 5. Key Design Decisions

### 1. **Substantial Extension of INET Showcase**
- **Original:** Generic flat wireless topology with identical nodes.
- **Extension:** Heterogeneous devices, dedicated gateway, wired core network, two traffic classes.

### 2. **Traffic Classes**
- **Periodic monitoring:** Temperature, humidity, motion (low-priority, best-effort).
- **Event-driven/critical:** Smoke/alarm (high-priority, latency-sensitive).

### 3. **Communication Strategies (Exp 4)**
- **Publish/Subscribe (MQTT-like):** Sensors initiate; lower latency, higher traffic.
- **Request/Response (CoAP-like):** Server polls; lower traffic, higher latency.

### 4. **Fragmentation Study (Exp 5)**
- IEEE 802.15.4 PSDU limit is 127 octets.
- With IPv6 (40 octets) + UDP (8 octets) = 48-byte overhead minimum.
- Payloads >60 B trigger 6LoWPAN compression; >80 B may trigger fragmentation.
- Study quantifies airtime, delay, and PDR degradation.

### 5. **Multiple Seeds**
- Each experiment uses 5 independent random seeds to ensure reproducibility and statistical confidence.

---

## 6. Reproducibility Notes

### Software Environment
```
OMNeT++:        6.4.0 (built from source)
INET Framework: 4.5.4
Python:         3.12+ (for analysis scripts)
OS:             Linux (WSL supported)
```

### Build & Run Instructions

#### Setup (One-time)
```bash
cd /home/nawras/omnetpp-workspace

# Initialize OMNeT++ environment
source omnetpp-6.4.0/setenv

# Verify INET is linked
export INET_ROOT=/home/nawras/omnetpp-workspace/inet-4.5.4/src
```

#### Run a Single Experiment
```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject

# Example: Run Exp 1 with N=10 (all 5 seeds)
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  experiment1_scalability.ini -c Exp1_Scalability --param-study-index=0-4
```

#### Generate All Results
```bash
# Activate Python virtual environment
source .venv/bin/activate

# Run analysis scripts
python analyze_exp1.py
python analyze_exp2.py
python analyze_exp3.py
python analyze_exp4.py
python analyze_exp5.py

# Generate visualizations
python plot_exp1.py
python plot_exp2.py
python plot_exp3.py
python plot_exp4.py
python plot_exp5.py
```

### Output Locations
- **Simulation results:** `results/*.{sca,vec,vci}`
- **CSV summaries:** `results/exp{1..5}_{results,summary}.csv`
- **Plots:** `results/exp{1..5}_visualization.png`

### Key Assumptions
1. **Global ARP:** Simplified routing (all nodes know gateway location).
2. **Static routes:** Configurator computes routes at startup.
3. **No mobility:** All nodes are stationary.
4. **No obstacles:** Free-space propagation model.
5. **Background noise:** –110 dBm (simulates realistic RF environment).

---

## 7. Deliverables Checklist

- [x] **OMNeT++/INET Project**
  - [x] `.ned` files (2: SmartHomeNetwork, ScalabilityNetwork)
  - [x] `.ini` files (8 configurations)
  - [x] Run instructions

- [x] **Data Package**
  - [x] Raw simulation results (`.sca`, `.vec`, `.vci` files)
  - [x] Processed CSV summaries
  - [x] Seed information (5 seeds per run documented in `.ini`)
  - [x] Parameter sets (documented in `.ini` files)

- [ ] **Technical Report** (8–12 pages, to be written)
  - [ ] Model description
  - [ ] Assumptions
  - [ ] Experiment design
  - [ ] Results & analysis
  - [ ] Discussion
  - [ ] Limitations
  - [ ] Conclusion
  - [ ] References

- [ ] **Presentation** (10–12 slides, to be created)
  - [ ] Topology diagram
  - [ ] Protocol stack
  - [ ] Experimental design
  - [ ] 4–6 key plots
  - [ ] Conclusions

- [x] **Reproducibility Note** (this document)

---

## 8. Limitations & Caveats

1. **Simplified Protocol Stack:** UDP directly over IPv4/6LoWPAN (no TCP, CoAP, or MQTT protocol overhead modeling).
2. **Traffic Emulation:** Application patterns mimic CoAP/MQTT behavior but do not implement full protocol semantics.
3. **Energy Modeling:** Basic battery drain; no detailed per-device energy profiling in current scope.
4. **Interference:** Single-channel narrowband model; no multi-channel or coexistence analysis.
5. **Fragmentation Analysis:** Theoretically justified; simulation may not fully capture cross-layer fragmentation behavior in some scenarios.

---

## 9. Next Steps for Report & Presentation

### Report Structure
1. **Introduction:** IoT, smart-home applications, research questions.
2. **Related Work:** INET, IEEE 802.15.4, 6LoWPAN, CoAP/MQTT.
3. **Model & Methodology:** Topology, stack, experiments, metrics.
4. **Results:** Per-experiment analysis with plots and tables.
5. **Discussion:** Cross-layer insights, trade-offs, practical implications.
6. **Conclusion:** Key findings, future directions.

### Presentation Flow
1. **Slide 1:** Title, course, date.
2. **Slides 2–3:** Topology + stack diagram.
3. **Slides 4–5:** Experiment design overview.
4. **Slides 6–11:** Key results (1–2 plots per experiment).
5. **Slide 12:** Conclusions & limitations.

---

## 10. Contact & Responsibility Statement

**Project Team:** [Student Names — to be updated]  
**Supervisor:** [Professor Name — to be updated]  

### Responsibility Clause
**Students remain responsible for every design decision, implementation detail, analysis interpretation, and result presented in this work.** All team members must be able to explain the topology, stack assumptions, experiment design, and results in detail. Any external tools, code, or frameworks are duly cited, and the simulation boundaries are clearly defined.

---

**Last Updated:** September 1, 2026  
**Status:** Ready for deployment and evaluation
