from dragonfly import topology
from mininet.cli import CLI

from scapy.all import sniff
from scapy.layers.l2 import Ether

import threading
import time

from mac_switch import DragonflySwitch


# -----------------------------
# Create Model 2 Switch
# -----------------------------
dragon = DragonflySwitch()

# -----------------------------
# Packet Observer
# -----------------------------
def process_packet(pkt):

    if Ether in pkt:

        src_mac = pkt[Ether].src

        dragon.packet_observed(src_mac)


def start_sniffer():

    sniff(
        iface="g0_s0-eth1",
        prn=process_packet,
        store=False
    )


# -----------------------------
# Start Dragonfly
# -----------------------------
net = topology()
net.start()

print("\nMININET NETWORK STARTED")
print("-----------------------\n")

for sw in net.switches:
    sw.cmd(
        f'ovs-vsctl set-fail-mode {sw.name} standalone'
    )

# -----------------------------
# Hosts
# -----------------------------
h1 = net.get('g0_s0_h1')
h2 = net.get('g0_s1_h1')
h4 = net.get('g1_s1_h1')

# -----------------------------
# MAC Addresses
# -----------------------------
h1_mac = h1.MAC()
h2_mac = h2.MAC()
h4_mac = h4.MAC()

print("H1:", h1_mac)
print("H2:", h2_mac)
print("H4:", h4_mac)

# -----------------------------
# Learn MACs once
# -----------------------------
dragon.learn_mac(h1_mac, 1)
dragon.learn_mac(h2_mac, 2)
dragon.learn_mac(h4_mac, 3)

print("\nINITIAL MAC TABLE")
dragon.show_mac_table()

# -----------------------------
# Start Packet Monitoring
# -----------------------------
sniffer_thread = threading.Thread(
    target=start_sniffer,
    daemon=True
)

sniffer_thread.start()

time.sleep(2)

# -----------------------------
# Intra Group Traffic
# -----------------------------
print("\nINTRA GROUP TRAFFIC")
print("-------------------")

h1.cmd(
    f"ping -c 10 {h2.IP()}"
)

time.sleep(2)

# -----------------------------
# Inter Group Traffic
# -----------------------------
print("\nINTER GROUP TRAFFIC")
print("-------------------")

h1.cmd(
    f"ping -c 20 {h4.IP()}"
)

time.sleep(5)

# -----------------------------
# Results
# -----------------------------
print("\nUPDATED MAC TABLE")
dragon.show_mac_table()

# -----------------------------
# CLI
# -----------------------------
CLI(net)

# -----------------------------
# Stop Network
# -----------------------------
net.stop()

print("\nNETWORK STOPPED")