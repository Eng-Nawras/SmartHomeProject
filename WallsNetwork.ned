//
// Smart-Home IoT Network — OBSTACLES/WALLS BONUS EXTENSION
// Birzeit University, ENCS5325, Summer 2026
//
// Extends SmartHomeNetwork with a PhysicalEnvironment module representing
// an interior wall (concrete partition) that separates one room
// (containing temp1, smoke1, smoke2) from the rest of the house, including
// the gateway. This tests the Bonus criterion "obstacles/walls": how a
// physical obstruction attenuates the IEEE 802.15.4 signal and affects
// PDR/delay for the devices behind it — notably the smoke sensors, which
// carry the critical traffic class.
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
import inet.environment.common.PhysicalEnvironment;


network WallsNetwork
{
    parameters:
        @display("bgb=32,20");
    submodules:
        // ---------------- Periodic monitoring sensors ----------------
        temp1: SensorNode { @display("p=3,3;i=misc/sensor"); }      // behind the wall
        temp2: SensorNode { @display("p=3,7;i=misc/sensor"); }
        temp3: SensorNode { @display("p=3,11;i=misc/sensor"); }
        motion1: SensorNode { @display("p=3,15;i=misc/sensor2"); }
        motion2: SensorNode { @display("p=6,17;i=misc/sensor2"); }
        motion3: SensorNode { @display("p=9,17;i=misc/sensor2"); }

        // ---------------- Event-driven / critical sensors ----------------
        smoke1: SensorNode { @display("p=13,3;i=misc/sensor3"); }   // behind the wall
        smoke2: SensorNode { @display("p=17,3;i=misc/sensor3"); }   // behind the wall

        // ---------------- Actuators ----------------
        light1: SensorNode { @display("p=13,17;i=status/bulb"); }
        light2: SensorNode { @display("p=17,17;i=status/bulb"); }
        hvac1: SensorNode { @display("p=20,10;i=misc/thermometer"); }
        alarm1: SensorNode { @display("p=20,14;i=misc/alarm"); }

        // ---------------- Gateway / Border Router ----------------
        gateway: Router {
            numWlanInterfaces = 1;
            wlan[0].typename = "Ieee802154NarrowbandInterface";
            @display("p=10,10;i=misc/sensorgateway");
        }

        // ---------------- Wired core network ----------------
        coreSwitch: EthernetSwitch { @display("p=15,10"); }
        monitoringApp: StandardHost { @display("p=20,7;i=device/server"); }

        // ---------------- Wireless medium ----------------
        radioMedium: Ieee802154NarrowbandScalarRadioMedium { @display("p=28,1"); }

        // ---------------- BONUS: Physical environment (walls) ----------------
        physicalEnvironment: PhysicalEnvironment {
            @display("p=28,9");
        }

        // ---------------- IP configurator & visualizer ----------------
        configurator: Ipv4NetworkConfigurator { @display("p=28,3"); }
        visualizer: IntegratedMultiCanvasVisualizer { @display("p=28,5"); }

    connections:
        gateway.ethg++ <--> Eth1G <--> coreSwitch.ethg++;
        coreSwitch.ethg++ <--> Eth1G <--> monitoringApp.ethg++;
}
