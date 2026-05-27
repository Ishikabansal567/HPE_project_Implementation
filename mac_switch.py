import time

from dynamic_ttl import calculate_dynamic_ttl

class MACentry:
    def __init__(self,mac,port):

        self.mac = mac
        self.port= port

        self.ttl = 300
        self.tx_count = 0
        self.flap_count = 0

        # Time when MAC learned
        self.learned_time = time.time()

        # Last port for flap detection
        self.last_port = port

    #Updating the f_activity when packet is recieved
    def receive_packet(self):
        self.tx_count +=1   

    #updating flapping activity
    def check_flap(self, new_port):

        if self.last_port != new_port:
            self.flap_count+=1
            self.last_port = new_port
            self.port= new_port
    
    #ReCalculating dynamic ttl and also calculates the occupancy of
    #mac table
    def update_ttl(self,occupied):

        self.ttl = calculate_dynamic_ttl(
            tx_count = self.tx_count,
            flap_count = self.flap_count,
            occupied = occupied
        )
    
    #to show mac information table
    def show(self):
        
        print("MAC address: " ,self.mac)
        print("Port:",self.port)
        print("TX count:", self.tx_count)
        print("Flap count" , self.flap_count)
        print ("Dynamic TTL:" , self.ttl,"sec")
        print("\n--------------------\n")

class DragonflySwitch():

    def __init__(self):
         self.mac_table = {}
    
    def learn_mac(self, mac, port):
        if mac in self.mac_table:
            entry = self.mac_table[mac];

            #inncreasing f_activity
            entry.receive_packet()

            #checking flap activity
            entry.check_flap(port)

            entry.update_ttl(len(self.mac_table))

            print(f"Updated the exisiting mac: {mac}")

        else:
            #else we create a new object
            entry = MACentry(mac,port)

            #first packet received
            entry.receive_packet()

            entry.update_ttl(len(self.mac_table))

            #storing in mac table
            self.mac_table[mac]= entry

            print(f"learned new mac: {mac}")
        entry.show()    
            
    def remove_expired_entries(self):
        current_time = time.time()
        expired = []
        for mac , entry in self.mac_table.items():
            age  = current_time - entry.learned_time
            if age > entry.ttl:
                expired.append(mac)
        for mac in expired:
            print(f"Removing expired MAC: {mac}")
            del self.mac_table[mac]

        

    # def age_mac_table(self):
    #     current
    def show_mac_table(self):
        print("----MAC Table----")

        print("MAC | PORT | TX_COUNT | FLAP_COUNT | TTL")

        for entry in self.mac_table.values():

            print(f"MAC Address    : {entry.mac}")
            print(f"Port           : {entry.port}")
            print(f"TX Count       : {entry.tx_count}")
            print(f"Flap Count     : {entry.flap_count}")
            print(f"Dynamic TTL    : {entry.ttl}")
            print("---------------------------------")

        if not self.mac_table:
            print("MAC table empty")

        