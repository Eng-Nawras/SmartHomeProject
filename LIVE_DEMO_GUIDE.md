# TOPOLOGY LIVE DEMO GUIDE
## Smart-Home IoT Network (OMNeT++ Qtenv Visualization)

---

## 🎯 Quick Start

### Option A: Direct Command (Simplest)
```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject

# Set up OMNeT++ environment
source ../omnetpp-6.4.0/setenv

# Run topology viewer
opp_run -u Qtenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  test_network.ini -c TestNetwork
```

### Option B: Run Script
```bash
cd /home/nawras/omnetpp-workspace/SmartHomeProject
./run_topology_demo.sh
```

---

## 📊 What You'll See in Qtenv

### 1. **Network Topology Panel** (Left side)
```
SmartHomeNetwork
├── temp1, temp2, temp3
├── motion1, motion2, motion3
├── smoke1, smoke2
├── light1, light2
├── hvac1
├── alarm1
├── gateway (highlighted, bridge icon)
├── coreSwitch (switch icon)
├── monitoringApp (server icon)
├── radioMedium (wireless medium)
├── configurator (routing)
└── visualizer (display)
```

### 2. **Canvas** (Center)
- **Visual representation** of the network
- Nodes positioned in 2D space
- **Color coding:**
  - Blue: Temperature/Motion sensors
  - Red: Smoke/Alarm sensors
  - Yellow: Actuators
  - Green: Gateway
  - Orange: Wired core devices

### 3. **Animation Controls** (Top toolbar)
```
[Run] [Step] [Stop] [Speed slider] [Zoom] [Pan]
```

### 4. **Simulation Time** (Bottom)
```
Simulated time: 0s → 120s (as it progresses)
```

---

## 🔍 Interactive Features in Qtenv

### 1. **Inspect a Node**
- Double-click any node (e.g., `temp1`)
- Opens parameter inspector
- View:
  - IP address
  - Port number
  - Application type
  - Wireless interface config
  - Energy consumption

### 2. **Watch Packet Flow**
- Packets appear as **animated arrows**
- From sensors → gateway
- Gateway → core switch
- Core switch → monitoring app
- Shows **real-time data transfer**

### 3. **View Network Statistics**
- Right panel: Scalars (live updates)
  - Packets sent
  - Packets received
  - Average delay
  - Energy consumed

### 4. **Zoom & Pan**
- Scroll wheel: Zoom in/out
- Right-click drag: Pan around
- Fit to window: Press 'F'

### 5. **Adjust Simulation Speed**
- Speed slider (top right)
- Slow down to see packets clearly
- Speed up to see overall behavior

---

## 🎬 Typical Demo Workflow

### Step 1: Launch Qtenv
```bash
./run_topology_demo.sh
# or use the direct opp_run command above
```

### Step 2: Startup Dialog
- Appears: "Select simulation or run"
- Choose: **Exp1_Scalability: Default**
- Click "OK"

### Step 3: Initialization Phase
```
Loading NED files...
Loading images...
Setting up Qtenv...
Initializing simulation...
```
- Wait ~5-10 seconds

### Step 4: View Topology
- Network diagram appears on canvas
- All 12 nodes visible
- Gateway in center, sensors around, wired devices on right

### Step 5: Run Simulation
- Click **[Run]** button (or press spacebar)
- Packets start flowing (animated)
- Statistics update in real time

### Step 6: Inspect Details
- **Pause** simulation (click [Step])
- Double-click any node to inspect
- View current packet queue, energy, etc.

### Step 7: Stop & Exit
- Click **[Stop]** or close window
- Final statistics printed to console

---

## 💡 What Each Node Type Does

### Sensors (temp1–3, motion1–3)
```
Every 10 seconds:
- Generate application packet (50B)
- Package it in UDP
- Send to monitoringApp via gateway
- Wireless transmission (IEEE 802.15.4)
```

### Critical Sensors (smoke1–2)
```
On event (exponential distribution):
- Generate alarm packet
- Send immediately (high priority)
- Expect low latency
```

### Actuators (light1–2, hvac1, alarm1)
```
Idle listeners:
- Wait for commands from monitoringApp
- Receive control packets
- Act on instructions
```

### Gateway
```
Border Router:
- Receives wireless 802.15.4 packets
- Bridges to Ethernet
- Forwards to core network
- Translates between PHY layers
```

### Monitoring App
```
Central Sink/Broker:
- Listens on UDP port 5000
- Receives all sensor data
- Aggregates statistics
- Can send commands back
```

---

## 📈 Expected Behavior During Demo

### Packet Flow Pattern
```
Periodic:
temp1 → gateway → switch → monitoringApp (every 10s)
temp2 → gateway → switch → monitoringApp (every 10s)
... (all periodic sensors)

Event-Driven:
smoke1 → gateway → switch → monitoringApp (on alarm)
smoke2 → gateway → switch → monitoringApp (on alarm)
```

### Statistics You'll See
```
After 120s simulation:
- Total packets sent: ~70–80 (12 sensors × ~6–7 per node)
- Total packets received: ~60–75 (some loss possible)
- Average delay: ~0.1–0.5ms
- Energy consumed: Varies by node activity
```

---

## 🔧 Troubleshooting

### Problem: "X11 display not found" (WSL)
**Solution:**
1. Install VcXsrv on Windows
2. Start VcXsrv (check "Disable access control")
3. In WSL, export DISPLAY=:0
4. Run Qtenv

### Problem: "No Qt platform plugin found"
**Solution:**
```bash
export QT_QPA_PLATFORM=xcb
export LIBGL_ALWAYS_SOFTWARE=1
```

### Problem: "INET library not found"
**Solution:**
```bash
# Make sure INET_ROOT is set
export INET_ROOT=/home/nawras/omnetpp-workspace/inet-4.5.4/src
# and pass it to opp_run
-l $INET_ROOT/INET
```

### Problem: "Simulation won't start"
**Alternative:** Use Cmdenv (console) instead
```bash
opp_run -u Cmdenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  test_network.ini -c TestNetwork
```
(Won't show GUI, but proves the network works)

---

## 📸 Screenshots You Can Take

1. **Full Network View**
   - All 12 nodes visible
   - Gateway bridging wireless/wired
   - Clean topology layout

2. **Packet Flow**
   - Arrows between nodes
   - Multiple packets in flight
   - Shows concurrency

3. **Node Inspector**
   - Double-click any node
   - Shows IP, ports, application type
   - Energy consumption
   - Interface statistics

4. **Statistics Panel**
   - Scalars panel (right)
   - Live metric updates
   - PDR, delay, throughput

---

## 🎓 Key Learning Points from Demo

1. **Heterogeneous Network**
   - Wireless sensors (constrained)
   - Wired core (unconstrained)
   - Clear separation

2. **Gateway Role**
   - Bridges two domains
   - Visible in topology
   - Central routing point

3. **Traffic Classes**
   - Periodic (continuous)
   - Event-driven (sporadic)
   - Both coexist

4. **Cross-Layer Visibility**
   - See packet creation (app)
   - See transmission (MAC)
   - See arrival (app)

5. **Performance Metrics**
   - PDR (packet delivery)
   - Latency (delay)
   - Throughput (data rate)

---

## 📝 For Your Presentation

**Screenshot Suggestions:**
1. Qtenv main window with topology
2. Node inspector showing device details
3. Statistics panel showing live metrics
4. Zoomed-in view of gateway region

**Narration:**
> "The Qtenv window shows our 12-node smart-home network. 
> Periodic sensors (blue) send data every 10 seconds. 
> Critical sensors (red) emit events immediately. 
> All wireless traffic flows through the gateway to the 
> wired core network where the monitoring application 
> receives and aggregates the data."

---

## ⏱️ Demo Duration

- Setup: 30 seconds
- Launch: 10 seconds
- Inspect: 2–3 minutes
- Run simulation: 2–3 minutes
- **Total: ~5–7 minutes**

---

**Good luck with the demo! 🚀**

If you have questions during the demo, you can:
- Pause the simulation (click [Step])
- Inspect any node (double-click)
- Check statistics (look at scalars panel)
- Resume (click [Run])

---

Last Updated: September 1, 2026
