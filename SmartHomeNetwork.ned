//
// Smart-Home IoT Network — ENCS5325 Project
// Birzeit University, Summer 2026
//
// This network is a substantial extension of the official INET
// IEEE 802.15.4 Smart Home showcase (inet/showcases/wireless/ieee802154).
// Extensions over the original showcase:
//   - Heterogeneous device roster (temperature/humidity, motion/occupancy,
//     smoke/environmental sensors; light, HVAC, and alarm actuators)
//     instead of one generic "SensorNode" type repeated.
//   - A dedicated gateway/border router (Router, not a plain SensorNode)
//     bridging the 802.15.4 wireless side to a wired IP core network
//     (Ethernet), instead of a flat wireless-only topology.
//   - A wired core network with a switch and a Smart-Home Monitoring
//     Application host, representing the CoAP-like / MQTT-like
//     application server referred to in the project brief.
//   - Two explicit traffic classes: periodic monitoring traffic
//     (temperature/humidity/motion) and event-driven/critical traffic
//     (smoke/alarm), configured with different application parameters
//     in the .ini files.
//
package smarthome;

import inet.node.inet.SensorNode;
import inet.node.inet.StandardHost;
import inet.node.inet.Router;
import inet.node.ethernet.EthernetSwitch;
import inet.node.ethernet.Eth1G;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.physicallayer.wireless.ieee802154.packetlevel.Ieee802154NarrowbandScalarRadioMedium;
import inet.visualizer.canvas.integrated.IntegratedMultiCanvasVisualizer;


network SmartHomeNetwork
{
    parameters:
        @display("bgb=32,20");
    submodules:
        // ---------------- Periodic monitoring sensors ----------------
        temp1: SensorNode {
            @display("p=3,3;i=misc/sensor");
        }
        temp2: SensorNode {
            @display("p=3,7;i=misc/sensor");
        }
        temp3: SensorNode {
            @display("p=3,11;i=misc/sensor");
        }
        motion1: SensorNode {
            @display("p=3,15;i=misc/sensor2");
        }
        motion2: SensorNode {
            @display("p=6,17;i=misc/sensor2");
        }
        motion3: SensorNode {
            @display("p=9,17;i=misc/sensor2");
        }

        // ---------------- Event-driven / critical sensors ----------------
        smoke1: SensorNode {
            @display("p=13,3;i=misc/sensor3");
        }
        smoke2: SensorNode {
            @display("p=17,3;i=misc/sensor3");
        }

        // ---------------- Actuators ----------------
        light1: SensorNode {
            @display("p=13,17;i=status/bulb");
        }
        light2: SensorNode {
            @display("p=17,17;i=status/bulb");
        }
        hvac1: SensorNode {
            @display("p=20,10;i=misc/thermometer");
        }
        alarm1: SensorNode {
            @display("p=20,14;i=misc/alarm");
        }

        // ---------------- Gateway / Border Router ----------------
        gateway: Router {
            numWlanInterfaces = 1;
            wlan[0].typename = "Ieee802154NarrowbandInterface";
            @display("p=10,10;i=misc/sensorgateway");
        }

        // ---------------- Wired core network ----------------
        coreSwitch: EthernetSwitch {
            @display("p=15,10");
        }
        monitoringApp: StandardHost {
            @display("p=20,7;i=device/server");
        }

        // ---------------- Wireless medium ----------------
        radioMedium: Ieee802154NarrowbandScalarRadioMedium {
            @display("p=28,1");
        }

        // ---------------- IP configurator & visualizer ----------------
        configurator: Ipv4NetworkConfigurator {
            @display("p=28,3");
        }
        visualizer: IntegratedMultiCanvasVisualizer {
            @display("p=28,5");
        }

    connections:
        gateway.ethg++ <--> Eth1G <--> coreSwitch.ethg++;
        coreSwitch.ethg++ <--> Eth1G <--> monitoringApp.ethg++;
}
