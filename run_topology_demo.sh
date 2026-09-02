#!/bin/bash
# Set up environment
source /home/nawras/omnetpp-workspace/omnetpp-6.4.0/setenv

# Run the simulation with Qtenv (will show topology)
echo "=========================================="
echo "LAUNCHING TOPOLOGY VIEWER (Qtenv)"
echo "=========================================="
echo ""
echo "Network: SmartHomeNetwork (12-node)"
echo "Config: TestNetwork (Baseline)"
echo ""
echo "The Qtenv window should open in a few seconds..."
echo "You can:"
echo "  - Inspect network topology"
echo "  - Watch packet flow in real-time"
echo "  - Step through simulation"
echo "  - View node parameters"
echo ""
echo "=========================================="
echo ""

export DISPLAY=:0
export GDK_BACKEND=x11
export QT_QPA_PLATFORM=xcb
export LIBGL_ALWAYS_SOFTWARE=1

opp_run -u Qtenv \
  -n .:/home/nawras/omnetpp-workspace/inet-4.5.4/src \
  -l /home/nawras/omnetpp-workspace/inet-4.5.4/src/INET \
  test_network.ini -c TestNetwork

