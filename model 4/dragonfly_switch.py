# dragonfly_switch.py

import time

from dynamic_ttl import calculate_dynamic_ttl

from entry_eviction import (
    calculate_eviction_priority
)


# =====================================================
# MAC ENTRY
# =====================================================

class MACentry:

    def __init__(self, mac, port):

        self.mac = mac

        self.port = port

        self.ttl = 300

        self.tx_count = 0

        self.flap_count = 0

        self.learned_time = time.time()

        self.last_seen = time.time()

        self.last_port = port

    # -------------------------------------------------

    def receive_packet(self):

        self.tx_count += 1

        self.last_seen = time.time()

    # -------------------------------------------------

    def check_flap(self, new_port):

        if self.last_port != new_port:

            self.flap_count += 1

            self.last_port = new_port

            self.port = new_port

    # -------------------------------------------------

    def update_ttl(self, occupied):

        self.ttl = calculate_dynamic_ttl(
            tx_count=self.tx_count,
            flap_count=self.flap_count,
            occupied=occupied
        )

    # -------------------------------------------------

    def show(self):

        print(f"""
MAC Address : {self.mac}
Port        : {self.port}
TX Count    : {self.tx_count}
Flap Count  : {self.flap_count}
Dynamic TTL : {self.ttl} sec
""")


# =====================================================
# DRAGONFLY SWITCH
# =====================================================

class DragonflySwitch:

    def __init__(self):

        self.mac_table = {}

        self.MAX_MAC_ENTRIES = 3

        self.TTL_MAX = 300

    # -------------------------------------------------

    def learn_mac(self, mac, port):

        if mac in self.mac_table:

            entry = self.mac_table[mac]

            entry.receive_packet()

            entry.check_flap(port)

            entry.update_ttl(len(self.mac_table))

            print(f"\n[UPDATED EXISTING MAC] {mac}")

        else:

            # EVICT IF TABLE FULL
            if len(self.mac_table) >= self.MAX_MAC_ENTRIES:

                self.evict_entry()

            entry = MACentry(mac, port)

            entry.receive_packet()

            entry.update_ttl(len(self.mac_table))

            self.mac_table[mac] = entry

            print(f"\n[LEARNED NEW MAC] {mac}")

        entry.show()

    # -------------------------------------------------

    def evict_entry(self):

        highest_score = -1

        evict_mac = None

        current_time = time.time()

        print("\n========= EVICTION CHECK =========")

        for mac, entry in self.mac_table.items():

            age = current_time - entry.last_seen

            score = calculate_eviction_priority(
                age=age,
                ttl_max=self.TTL_MAX,
                tx_count=entry.tx_count,
                flap_count=entry.flap_count
            )

            print(f"""
MAC            : {mac}
Age            : {round(age, 2)}
TX Count       : {entry.tx_count}
Flap Count     : {entry.flap_count}
Priority Score : {score}
""")

            if score > highest_score:

                highest_score = score

                evict_mac = mac

        if evict_mac:

            print(f"\n[EVICTING MAC] {evict_mac}")

            del self.mac_table[evict_mac]

    # -------------------------------------------------

    def age_mac_table(self):

        current_time = time.time()

        expired = []

        for mac, entry in self.mac_table.items():

            age = current_time - entry.last_seen

            if age > entry.ttl:

                expired.append(mac)

        for mac in expired:

            print(f"\n[TTL EXPIRED] Removing {mac}")

            del self.mac_table[mac]

    # -------------------------------------------------

    def show_mac_table(self):

        print("\n================ MAC TABLE ================\n")

        if not self.mac_table:

            print("MAC Table Empty\n")

            return

        for entry in self.mac_table.values():

            entry.show()


# =====================================================
# MAIN TESTING
# =====================================================

if __name__ == "__main__":

    switch = DragonflySwitch()

    # -------------------------------------------------
    # LEARNING MACS
    # -------------------------------------------------

    switch.learn_mac("00:00:00:00:00:01", 1)

    time.sleep(1)

    switch.learn_mac("00:00:00:00:00:02", 2)

    time.sleep(1)

    switch.learn_mac("00:00:00:00:00:03", 3)

    # -------------------------------------------------
    # GENERATE TRAFFIC
    # -------------------------------------------------

    switch.learn_mac("00:00:00:00:00:01", 1)

    switch.learn_mac("00:00:00:00:00:01", 1)

    switch.learn_mac("00:00:00:00:00:02", 2)

    # -------------------------------------------------
    # MAC FLAPPING
    # -------------------------------------------------

    switch.learn_mac("00:00:00:00:00:03", 5)

    switch.learn_mac("00:00:00:00:00:03", 7)

    # -------------------------------------------------
    # THIS SHOULD TRIGGER EVICTION
    # -------------------------------------------------

    switch.learn_mac("00:00:00:00:00:04", 4)

    # -------------------------------------------------
    # SHOW FINAL TABLE
    # -------------------------------------------------

    switch.show_mac_table()