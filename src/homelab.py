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
        with Cluster("Docker Host 1"):
            pihole =  Custom ("Pihole", "img/pihole.png")
            openspeedtest =  Custom ("Open Speed Test", "img/openspeedtest.png")
            immich =  Custom ("Immich", "img/immich.png")
            traefik1 = Traefik("Traefik-1")
            dockerhost1 = [traefik1, pihole, openspeedtest, immich]
        with Cluster("Docker Host 2"): 
            unifi =  Custom ("Unifi Network Controller", "img/unifi.png")
            traefik2 = Traefik("Traefik-2")
            dockerhost2 = [traefik2, unifi]
        Ubuntu("Docker Host 1") - dockerhost1
        Ubuntu("Docker Host 2") - dockerhost2
        truenas