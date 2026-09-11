# Smart Home IoT Network Simulation

A simulation-based study of a smart-home IoT network using OMNeT++ 6.4.0 and INET 4.5.4.

The project evaluates an IEEE 802.15.4-based constrained wireless network connected through a gateway to an IPv4 monitoring/core network.

## Project Overview

The simulated smart home contains temperature sensors, motion sensors, smoke sensors, smart lights, an HVAC controller, an alarm device, an IEEE 802.15.4 gateway, and an IP/core monitoring application.

## Tools

- OMNeT++ 6.4.0
- INET Framework 4.5.4
- NED / C++
- Python
- Pandas
- Matplotlib
- Linux / WSL Ubuntu

## Experiments

### Experiment 1 - Scalability

Node count is varied across 5, 10, 20, 30, and 40 nodes. Five repetitions are used for each configuration.

### Experiment 2 - Reporting Interval

Reporting intervals are 1 s, 5 s, 10 s, 30 s, and 60 s. The experiment studies the trade-off between reporting frequency, network performance, and energy consumption.

### Experiment 3 - Critical Event under Background Traffic

Background traffic intensity is varied while critical/event-driven traffic is generated. The experiment evaluates critical-event delay and delivery behavior under increasing background traffic. No dedicated QoS or priority queue is claimed.

### Experiment 4 - Application Communication Strategy

Request/Response and Publish/Subscribe traffic patterns are compared using UDP applications. These are not implementations of MQTT or CoAP.

### Experiment 5 - Packet Size and Fragmentation Study

Payload sizes of 20 B, 50 B, 100 B, 200 B, and 400 B are evaluated. The simulation studies IEEE 802.15.4 frame transmission behavior. IPv6/6LoWPAN is not implemented; therefore, the 6LoWPAN discussion is an analytical comparison based on IEEE 802.15.4 constraints and 6LoWPAN specifications.

### Bonus 1 - Mobility

Random waypoint mobility is evaluated at 0, 0.5, 1, 1.5, and 2 m/s.

### Bonus 2 - Obstacles / Walls

No-wall and wall/obstacle configurations are compared using an ideal obstacle-loss mechanism. This represents binary blockage rather than detailed concrete-wall attenuation.

### Bonus 3 - Advanced Energy Modeling

An advanced radio-energy experiment uses state-based power-consumption parameters inspired by CC2420-class IEEE 802.15.4 radios. Radio power vectors are integrated over simulation time.

### Bonus 4 - Wi-Fi Coexistence

A shared dimensional radio medium is used to study Wi-Fi traffic coexisting with IEEE 802.15.4 smart-home traffic under No Wi-Fi, Low, Medium, and High loads.

## Reproducibility

Experiments use multiple repetitions with different simulation seeds. Analysis and plotting scripts are provided for Experiments 1-9.

Example:

```text
opp_run -u Cmdenv -n .:../inet-4.5.4/src -l ../inet-4.5.4/src/libINET.so -f experiment1_scalability.ini -c Exp1_Scalability
```

## Modeling Scope

### Implemented

- IEEE 802.15.4 wireless communication
- IPv4 network configuration
- UDP application traffic
- Smart-home sensor/actuator traffic
- Gateway and IP monitoring network
- Mobility
- Ideal obstacle blocking
- Radio energy modeling
- Dimensional Wi-Fi/802.15.4 coexistence

### Not directly implemented

- IPv6
- 6LoWPAN adaptation layer
- RFC 4944 fragmentation inside a 6LoWPAN module
- RFC 6282 IPHC processing
- Actual MQTT protocol
- Actual CoAP protocol
- Dedicated critical-traffic QoS/priority queues

These limitations are considered when interpreting the experimental results.

## Results

The results directory contains experiment summaries and visualization outputs. Large raw simulation result files are excluded from normal version control where appropriate.

## Academic Context

This project was developed for the Wireless Sensor Networks and Internet of Things course at Birzeit University. External protocol specifications, INET documentation, and other referenced material should be cited in the final technical report.
