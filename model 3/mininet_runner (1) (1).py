# mininet_runner.py

from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo
from mininet.cli import CLI

from dragonfly_switch import DragonflySwitch

import time


def run():

    topo = SingleSwitchTopo(k=4)

    net = Mininet(topo=topo)

    net.start()

    print("\n===== MININET STARTED =====\n")

    switch = DragonflySwitch()

    hosts = net.hosts

    # ------------------------------------------------
    # SIMULATE MAC LEARNING
    # ------------------------------------------------

    for i, host in enumerate(hosts):

        mac = host.MAC()

        port = i + 1

        switch.learn_mac(mac, port)

        time.sleep(1)

    # ------------------------------------------------
    # GENERATE SOME TRAFFIC
    # ------------------------------------------------

    print("\n===== GENERATING TRAFFIC =====\n")

    hosts[0].cmd("ping -c 2 %s" % hosts[1].IP())

    switch.learn_mac(hosts[0].MAC(), 1)

    switch.learn_mac(hosts[0].MAC(), 1)

    switch.learn_mac(hosts[1].MAC(), 2)

    # ------------------------------------------------
    # MAC FLAPPING
    # ------------------------------------------------

    print("\n===== SIMULATING FLAPPING =====\n")

    switch.learn_mac(hosts[2].MAC(), 5)

    switch.learn_mac(hosts[2].MAC(), 7)

    # ------------------------------------------------
    # THIS SHOULD TRIGGER EVICTION
    # ------------------------------------------------

    print("\n===== ADDING EXTRA MAC =====\n")

    switch.learn_mac("00:00:00:00:00:99", 9)

    # ------------------------------------------------
    # SHOW FINAL MAC TABLE
    # ------------------------------------------------

    switch.show_mac_table()

    CLI(net)

    net.stop()


if __name__ == "__main__":
    run()