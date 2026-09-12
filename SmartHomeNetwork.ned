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
        @display("bgb=42,28");
    submodules:
        // ---------------- Periodic monitoring sensors ----------------
        temp1: SensorNode {
            @display("p=4,5;i=misc/thermometer_l;is=18");
        }
        temp2: SensorNode {
            @display("p=4,12;i=misc/thermometer_l;is=18");
        }
        temp3: SensorNode {
            @display("p=4,19;i=misc/thermometer_l;is=18");
        }
        motion1: SensorNode {
            @display("p=11,20;i=misc/sensor2_l;is=18");
        }
        motion2: SensorNode {
            @display("p=17,20;i=misc/sensor2_l;is=18");
        }
        motion3: SensorNode {
            @display("p=23,20;i=misc/sensor2_l;is=18");
        }

        // ---------------- Event-driven / critical sensors ----------------
        smoke1: SensorNode {
            @display("p=12,5;i=misc/sensor3_l;is=18");
        }
        smoke2: SensorNode {
            @display("p=19,5;i=misc/sensor3_l;is=18");
        }

        // ---------------- Actuators ----------------
        light1: SensorNode {
            @display("p=28,19;i=status/bulb;is=18");
        }
        light2: SensorNode {
            @display("p=34,19;i=status/bulb;is=18");
        }
        hvac1: SensorNode {
            @display("p=30,6;i=misc/thermometer_l;is=18");
        }
        alarm1: SensorNode {
            @display("p=34,15;i=misc/fire_vs;is=18");
        }

        // ---------------- Gateway / Border Router ----------------
        gateway: Router {
            numWlanInterfaces = 1;
            wlan[0].typename = "Ieee802154NarrowbandInterface";
            @display("p=23,12;i=misc/sensorgateway_l;is=20");
        }

        // ---------------- Wired core network ----------------
        coreSwitch: EthernetSwitch {
            @display("p=30,12;i=device/switch_l;is=20");
        }
        monitoringApp: StandardHost {
            @display("p=37,12;i=device/server_l;is=22");
        }

        // ---------------- Wireless medium ----------------
        radioMedium: Ieee802154NarrowbandScalarRadioMedium {
            @display("p=41,2;is=0");
        }

        // ---------------- IP configurator & visualizer ----------------
        configurator: Ipv4NetworkConfigurator {
            @display("p=41,4;is=0");
        }
        visualizer: IntegratedMultiCanvasVisualizer {
            @display("p=41,6;is=0");
        }

    connections:
        gateway.ethg++ <--> Eth1G <--> coreSwitch.ethg++;
        coreSwitch.ethg++ <--> Eth1G <--> monitoringApp.ethg++;
}
