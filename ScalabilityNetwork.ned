//
// Scalable Smart-Home network for Experiment 1 (Network Scalability).
// Uses a parametric array of generic sensor nodes (numNodes) instead of
// fixed named devices, so the node count can be swept (N = 5,10,20,30,40)
// from the .ini file while packet size and reporting interval stay fixed.
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


network ScalabilityNetwork
{
    parameters:
        int numNodes = default(12);
        @display("bgb=30,20");
    submodules:
        node[numNodes]: SensorNode {
            @display("p=3,3");
        }
        gateway: Router {
            numWlanInterfaces = 1;
            wlan[0].typename = "Ieee802154NarrowbandInterface";
            @display("p=15,10;i=misc/sensorgateway");
        }
        coreSwitch: EthernetSwitch {
            @display("p=20,10");
        }
        monitoringApp: StandardHost {
            @display("p=25,7;i=device/server");
        }
        radioMedium: Ieee802154NarrowbandScalarRadioMedium {
            @display("p=28,1");
        }
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
