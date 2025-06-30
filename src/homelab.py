# diagram.py
from diagrams import Diagram, Cluster
from diagrams.onprem.proxmox import Pve
from diagrams.generic.network import Firewall, Switch, Subnet
from diagrams.custom import Custom
from diagrams.generic.os import Ubuntu
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Traefik

from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB

graph_attr = {
    "bgcolor": "transparent"
}

with Diagram("Network", show=False, graph_attr=graph_attr ):
    with Cluster("Internet"):
        wan1 = Custom("WAN1", "img/wan.png")
        wan2 = Custom("WAN2", "img/wan.png")
    with Cluster("10.2.50.1/24"):    
        mikrotik = Custom("Mikrotik","img/mikrotik.png")
        [wan1,wan2] >> mikrotik >> Switch("TP-Link Switch 2.5G") >> Pve("Proxmox-Hypervisor")

with Diagram("Apps", show=False, graph_attr=graph_attr):
    with Cluster("Proxmox"):
         truenas = Custom("Truenas Scale", "img/truenas.png")
         pihole =  Custom ("Pihole", "img/pihole.png")
         openspeedtest =  Custom ("Open Speed Test", "img/openspeedtest.png")
         unifi =  Custom ("Unifi Network Controller", "img/unifi.png")
         immich =  Custom ("Immich", "img/immich.png")
         Ubuntu("Docker Host 1") >> [Traefik("Traefik-1"), pihole, immich, openspeedtest]
         Ubuntu("Docker Host 2") >> [Traefik("Traefik-2"), unifi]
         truenas