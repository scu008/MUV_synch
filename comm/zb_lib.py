import serial
import binascii

class Xbee:
    
    def __init__(self, port, baud_rate = 9600):
        self.ser = serial.Serial(port, baud_rate)
        self.addr = '000000000000FFFF'
        
        # Socket property
        self.protocol = 'ZigBee'


    # function to send TX request packet 
    def send(self, string):  
    ######  User Data #######
        dest_64bit = self.addr
        dest_16bit = 'FFFE'
        rf_data = string + ' \n'
        #########################
         
        ## convert RF data to hex
        rf_hex = binascii.hexlify(rf_data)
        ##print "rf_hex=", rf_hex
        
         
        ## calculate packet length
        hex_len = hex(14 + (len(rf_hex)/2))
        hex_len = hex_len.replace('x','0')
        ##print "hex_len=", hex_len
         
         
        ## calculate checksum
        ## 0x17 is the sum of all parameters minus 64bit & 16bit dest addr & payload 
        checksum = 17
        for i in range(0,len(dest_64bit),2):
            checksum = checksum + int(dest_64bit[i:i+2],16)
         
        for i in range(0,len(dest_16bit),2):
            checksum = checksum + int(dest_16bit[i:i+2],16)
         
        for i in range(0,len(rf_hex),2):
            checksum = checksum + int(rf_hex[i:i+2],16)
         
         
        ## checksum = 0xFF - 8-bit sum of bytes between the length and checksum
        checksum = checksum%256
        checksum = 255 - checksum
        checksum = hex(checksum)
        checksum = checksum[-2:]
        checksum = checksum.replace('x','0')
         
         
        ## designing packet
        tx_req = ("7E" + hex_len + "10" + "01" + dest_64bit
                  + dest_16bit + "00" + "00" + rf_hex + checksum)
        tx_req = tx_req.upper()
        
        
        print('\n"' + string + '" -> ' + self.addr)
        print("Tx packet = ", tx_req + '\n')
        
         
         
        ## convert packet from hex to binary
        data = binascii.unhexlify(tx_req)
         
         
        ## send data on serial line to device
        self.ser.write(data)
    
    
        
    # function to receive packet
    def recv(self):
        
        data = self.ser.readline()
        
        packet_hex = binascii.hexlify(data)
        packet_hex = packet_hex.upper()
        packet_len = len(packet_hex)
        
        # Error message
        text = 'Error - Rx packet: ' + packet_hex
        
        
        # Check the number of start delimiter
        check = 0
        idx_list = []
        
        for i in range(0, len(packet_hex)):
            if packet_hex[i:i+2] == '7E':
                
                check = check + 1
                idx_list.append(i)
                
                
        
        # Determine frame start
        if check == 0 :
            idx = 0
        else :
            idx = idx_list[check-1]
                
                
        # Source address
        addr_64 = packet_hex[idx+8 : idx+24]
        addr_16 = packet_hex[idx + 14 : idx + 18]
               
                
        # received text (Transmit Request frame)
        text = binascii.unhexlify( packet_hex[idx + 30 : packet_len-4] )
        return text
     
     
     
     
     # function for AT command
    def find_addr(self):
        
        # Send AT command
        sh_comm = binascii.unhexlify('7E0004080153485B')
        sl_comm = binascii.unhexlify('7E00040801534C57')
        
        # Receive command results
        self.ser.write(sh_comm)
        sh_result = binascii.hexlify( self.ser.read(13) )
        self.ser.write(sl_comm)
        sl_result = binascii.hexlify( self.ser.read(13) )
        
        # Processing the results
        addr = sh_result[-10:-2] + sl_result[-10:-2]
        
        
        return addr.upper()
         
     
     
     
     
     