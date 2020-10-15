from bluetooth import *
from os import system


class bt_socket():
    
    def __init__(self):
        system('sudo hciconfig')
        system('sudo hciconfig hci0 up')        # Enables bt on this device
        system('sudo hciconfig hci0 piscan')    # Gets UUID of devices in pairing mode
        
        # Socket property
        self.protocol = 'Bluetooth'
        
        
        
    def listen(self, name_str):
        services = find_service(name = name_str, uuid = SERIAL_PORT_CLASS)

        for i in range(len(services)):
            match = services[i]
            if(match["name"] == name_str):
                port = match["port"]
                name = match["name"]
                host = match["host"]
                
                print name, port, host
                
                socket = BluetoothSocket( RFCOMM )
                socket.connect((host, port))
                
                return socket
            
            
    def advertise(self, name_str):
            
        # Open serial & broadcast coordinator addr
        sock = BluetoothSocket( RFCOMM )
    
        sock.bind(("",PORT_ANY))
        sock.listen(1)
    
        advertise_service(server_sock, name_str, service_classes=[SERIAL_PORT_CLASS], profiles=[SERIAL_PORT_PROFILE])
    
    
        socket, address = sock.accept()
        return socket
        
        print "Accepted connection from ", address
            
            
    