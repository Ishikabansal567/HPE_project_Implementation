from dragonfly_topology import build_dragonfly, install_normal_flows
from ovs_fdb_monitor import FDBMonitor
from zscore_detector import calculate_zscores

import time


# FIX: STP needs time to converge on a looped topology before any
# MAC learning or meaningful traffic can occur.
STP_CONVERGENCE_WAIT = 15  # seconds


def run():

    net = build_dragonfly()

    net.start()

    print("\n===== MODEL 4 STARTED =====\n")

    # FIX: install NORMAL action flows so OVS runs in MAC-learning
    # mode and fdb/show actually returns entries
    print("[*] Installing NORMAL flows on all switches...")
    install_normal_flows(net)

    # FIX: wait for STP to converge before starting traffic/monitoring
    print(f"[*] Waiting {STP_CONVERGENCE_WAIT}s for STP to converge...")
    time.sleep(STP_CONVERGENCE_WAIT)

    # Trigger initial MAC learning by pinging all hosts
    print("[*] Running pingAll to seed the FDB tables...")
    net.pingAll()

    monitor = FDBMonitor()

    try:

        while True:

            flap_counts = monitor.update()

            print("\nFlap Counts:")
            print(flap_counts)

            zscores = calculate_zscores(flap_counts)

            for mac, z in zscores.items():

                if z > 2:

                    print("\n====================")
                    print("[ALERT]")
                    print(f"MAC = {mac}")
                    print(f"Flaps = {flap_counts[mac]}")
                    print(f"Z-score = {z}")
                    print("====================\n")

            time.sleep(5)

    except KeyboardInterrupt:

        net.stop()


if __name__ == "__main__":

    run()