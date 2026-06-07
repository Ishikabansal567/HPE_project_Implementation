from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel

from dragonfly import topology
from mac_switch import DragonflySwitch

import time

def run():

    print ("Dragonfly topology started")
    switch = DragonflySwitch()

    #case 1: for stable and active mac entry

    print("active+stable mac entry")
    for i in range(20):
        switch.learn_mac(
            mac = "AA:BB:CC:DD",
            port =1
        )
        time.sleep(0.2)
        print("\n------------")

    print("flapping mac")
    ports = (1,2,3,1,4,2)
    for p in ports:
        switch.learn_mac(
            mac = "11:22:33:44", 
            port =p
        )
        time.sleep(0.5)
        print("\n ----------")
    print ("final MAC Table:")    
    switch.show_mac_table()

    topology()
    

if __name__ == "__main__":

    setLogLevel("info")
    run()    