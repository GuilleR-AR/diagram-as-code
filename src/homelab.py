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
        switch = Switch("TP-Link Switch 2.5G")
        ap = Custom("Unifi AP", "img/unifiap-u6-lite.png")

        [wan1,wan2] >> mikrotik >> switch >> [Pve("Proxmox-Hypervisor"), Pve("Proxmox-Hypervisor2"), ap]

with Diagram("Apps", show=False, graph_attr=graph_attr):
    with Cluster("Proxmox"):
        truenas = Custom("Truenas Scale", "img/truenas.png")
        with Cluster("Docker Host 1"):
            pihole =  Custom ("Pihole", "img/pihole.png")
            openspeedtest =  Custom ("Open Speed Test", "img/openspeedtest.png")
            immich =  Custom ("Immich", "img/immich.png")
            traefik1 = Traefik("Traefik-1")
            dockerhost1 = [traefik1, pihole, openspeedtest, immich]
        Ubuntu("Docker Host 1") - dockerhost1
        truenas
    with Cluster("Proxmox2"):
        with Cluster("Docker Host 2"):
            pihole2 =  Custom ("Pihole2", "img/pihole.png") 
            unifi =  Custom ("Unifi Network Controller", "img/unifi.png")
            uptimekuma = Custom ("Uptime Kuma", "img/uptimekuma.png")
            traefik2 = Traefik("Traefik-2")
            dockerhost2 = [pihole2, traefik2, unifi, uptimekuma]
        Ubuntu("Docker Host 2") - dockerhost2

with Diagram("Homelab", show=False, graph_attr=graph_attr):
    with Cluster("Homelab"):
        with Cluster("Internet"):
            wan1 = Custom("WAN1", "img/wan.png")
            wan2 = Custom("WAN2", "img/wan.png")
        with Cluster("10.2.50.1/24"):    
            mikrotik = Custom("Mikrotik","img/mikrotik.png")
            switch = Switch("TP-Link Switch 2.5G")
            ap = Custom("Unifi AP", "img/unifiap-u6-lite.png")
            with Cluster("Proxmox"):
                truenas = Custom("Truenas Scale", "img/truenas.png")
                with Cluster("Docker Host 1"):
                    pihole =  Custom ("Pihole", "img/pihole.png")
                    openspeedtest =  Custom ("Open Speed Test", "img/openspeedtest.png")
                    immich =  Custom ("Immich", "img/immich.png")
                    traefik1 = Traefik("Traefik-1")
                    dockerhost1 = [traefik1, pihole, openspeedtest, immich]
                switch - Ubuntu("Docker Host 1") - dockerhost1
                switch - truenas
            with Cluster("Proxmox2"):
                with Cluster("Docker Host 2"): 
                    pihole2 =  Custom ("Pihole2", "img/pihole.png")
                    unifi =  Custom ("Unifi Network Controller", "img/unifi.png")
                    uptimekuma = Custom ("Uptime Kuma", "img/uptimekuma.png")
                    traefik2 = Traefik("Traefik-2")
                    dockerhost2 = [pihole2, traefik2, unifi, uptimekuma]
                switch - Ubuntu("Docker Host 2") - dockerhost2
            [wan1,wan2] >> mikrotik >> switch >> ap
            