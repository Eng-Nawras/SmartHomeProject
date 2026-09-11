//
// Bonus 4 - IEEE 802.11 / IEEE 802.15.4 Coexistence
// ENCS5325 Wireless Sensor Networks and Internet of Things
//

package smarthome;

import inet.node.inet.SensorNode;
import inet.node.inet.StandardHost;
import inet.node.inet.Router;
import inet.node.inet.AdhocHost;
import inet.node.ethernet.EthernetSwitch;
import inet.node.ethernet.Eth1G;
import inet.networklayer.configurator.ipv4.Ipv4NetworkConfigurator;
import inet.physicallayer.wireless.common.medium.RadioMedium;
import inet.visualizer.canvas.integrated.IntegratedMultiCanvasVisualizer;

network WifiCoexistenceNetwork
{
    parameters:
        @display("bgb=40,24");

    submodules:
        // ==================== 802.15.4 Smart Home ====================

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

        smoke1: SensorNode {
            @display("p=13,3;i=misc/sensor3");
        }
        smoke2: SensorNode {
            @display("p=17,3;i=misc/sensor3");
        }

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

        gateway: Router {
            numWlanInterfaces = 1;
            wlan[0].typename = "Ieee802154NarrowbandInterface";
            @display("p=10,10;i=misc/sensorgateway");
        }

        // ==================== Wired core ====================

        coreSwitch: EthernetSwitch {
            @display("p=26,10");
        }

        monitoringApp: StandardHost {
            @display("p=32,7;i=device/server");
        }

        // ==================== Wi-Fi interferer ====================
        // Two 802.11 ad-hoc hosts generate traffic on the same
        // dimensional wireless medium.

        wifiHost1: AdhocHost {
            @display("p=31,17;i=device/laptop");
        }

        wifiHost2: AdhocHost {
            @display("p=37,17;i=device/laptop");
        }

        // ==================== Shared dimensional medium ====================

        radioMedium: RadioMedium {
            @display("p=37,2");
        }

        configurator: Ipv4NetworkConfigurator {
            @display("p=37,4");
        }

        visualizer: IntegratedMultiCanvasVisualizer {
            @display("p=37,6");
        }

    connections:
        gateway.ethg++ <--> Eth1G <--> coreSwitch.ethg++;
        coreSwitch.ethg++ <--> Eth1G <--> monitoringApp.ethg++;
}
