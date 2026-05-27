# main.py

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

from dragonfly import topology
from mac_switch import DragonflySwitch

import time


def run():

    print("\n========== Dragonfly Topology Started ==========\n")

    # Create switch object
    switch = DragonflySwitch()

    # ------------------------------------------------
    # CASE 1 : Stable and Active MAC
    # ------------------------------------------------

    print("\n[CASE 1] Stable + Active MAC Entry\n")

    for i in range(20):

        switch.learn_mac(
            mac="AA:BB:CC:DD",
            port=1
        )

        time.sleep(0.2)

    # ------------------------------------------------
    # CASE 2 : Flapping MAC
    # ------------------------------------------------

    print("\n[CASE 2] Flapping MAC Entry\n")

    ports = [1, 2, 3, 1, 4, 2]

    for p in ports:

        switch.learn_mac(
            mac="11:22:33:44",
            port=p
        )

        time.sleep(0.5)

    # ------------------------------------------------
    # FINAL MAC TABLE
    # ------------------------------------------------

    print("\n========== FINAL MAC TABLE ==========\n")

    switch.show_mac_table()

    # Start Dragonfly topology
    topology()


if __name__ == "__main__":

    setLogLevel("info")

    run()