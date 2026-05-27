# mininet_test.py

from mininet.net import Mininet
from dragonfly import topology
from mininet.cli import CLI

import time

# Import your switch model
from mac_switch import DragonflySwitch


# Created Dragonfly switch object
dragon = DragonflySwitch()

net = topology()
net.start()

# Start network
print(net.hosts)

print(" MININET NETWORK STARTED ")
print("-------------------------\n")
for switch in net.switches:
    switch.cmd(f'ovs-vsctl set-fail-mode {switch.name} standalone')

# Get hosts
h1 = net.get('g0_s0_h1')
h2 = net.get('g0_s1_h1')


# Get real MAC addresses
h1_mac = h1.MAC()
h2_mac = h2.MAC()

print("H1 MAC Address:", h1_mac)
print("H2 MAC Address:", h2_mac)

# Learn MAC addresse
dragon.learn_mac(
    mac=h1_mac,
    port=1
)

dragon.learn_mac(
    mac=h2_mac,
    port=2
)

# Show MAC tabl
print("\n--INITIAL MAC TABLE --")

dragon.show_mac_table()

#Generating Traffic
print("\n --- Generating traffic --- ")
result  = h1.cmd('ping -c 2 10.0.0.2')
print (result)

#waiting for ttl expiry
print("\n--- waiting for ttl expiry")
time.sleep(20)

print("\n---REMOVING EXPIRED ENTRIES--")
dragon.remove_expired_entries()

#show updated MAC Table
print("\n -- Updated MAC table")
dragon.show_mac_table()


# # Optional flap tes
# print("\n--FLAP TEST--")

# dragon.learn_mac(
#     mac=h1_mac,
#     port=2
# )

# dragon.learn_mac(
#     mac=h1_mac,
#     port=1
# )

# dragon.show_mac_table()

# Open Mininet CLI
time.sleep(30)
print("\n[+] Testing Dragonfly Connectivity...")
net.pingAll(timeout = 0.5)

CLI(net)

# Stop networ
net.stop()

print("\n--NETWORK STOPPED --")