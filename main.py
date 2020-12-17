import os
import socket
import sys
from threading import Thread
import time


# function responsible for receiving and processing UDP packets from peers

def GetUdpChatMessage():
    global name
    global broadcastSocket
    global current_online
    while True:
        recv_message = broadcastSocket.recv(1024)              
        recv_string_message = str(recv_message.decode('utf-8'))
        if recv_string_message.find(':') != -1:                
        
            print('\r%s\n' % recv_string_message, end='')      
        elif recv_string_message.find('!@#') != -1 and recv_string_message.find(':') == -1 and recv_string_message[3:] in current_online:
      
            current_online.remove(recv_string_message[3:])   
            print('>> Online now: ' + str(len(current_online))) 
        elif not(recv_string_message in current_online) and recv_string_message.find(':') == -1:
     
            current_online.append(recv_string_message)      
            print('>> Online now: ' + str(len(current_online)))

# function responsible for sending messages to all peers
def SendBroadcastMessageForChat():
    global name
    global sendSocket
    sendSocket.setblocking(False)         
    while True:                          
        data = input()                 
        if data == 'Output()':               
      
            close_message = '!@#' + name  
            sendSocket.sendto(close_message.encode('utf-8'), ('255.255.255.255', 8080))
            #time.sleep(2)               
            os._exit(1)                    
        elif data != '' and data != 'Output()':  
       
            send_message = name + ': ' + data 
            sendSocket.sendto(send_message.encode('utf-8'), ('255.255.255.255', 8080)) 
        else:
      
            print('Write a message first!')        


def SendBroadcastOnlineStatus():
    global name
    global sendSocket
    sendSocket.setblocking(False)          
    while True:                            
        time.sleep(1)                    
        sendSocket.sendto(name.encode('utf-8'), ('255.255.255.255', 8080)) 


def main():
    global broadcastSocket
  
    broadcastSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
    broadcastSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
    broadcastSocket.bind(('0.0.0.0', 8080))                                
    global sendSocket
 
    sendSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           # initializing a socket to work with IPv4 addresses using UDP
    sendSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)         # we assign the SO_BROADCAST parameter at the library level, SO_BROADCAST - indicates that the packets will be broadcast

  
    print('*************************************************')
    print('*  Welcome To a Version 1 P2P Chat !              *')
    print('*  To log out, send a message: Log out ()    *')
    print('*  After entering the name, you can immediately write to the chat.  *')
    print('*  !                *')
    print('*************************************************')


    global name
    name = ''                                               
    # accurate, but poor implementation of username input

    while True:                                                 
        if not name:

            name = input('Name: ')
            if not name:
            # If name is empty 
                print('Please enter a non-blank name!')
            else:

                break
    print('*************************************************')  

    global recvThread
    recvThread = Thread(target=GetUdpChatMessage)             

    global sendMsgThread
    sendMsgThread = Thread(target=SendBroadcastMessageForChat)  
    global current_online
    current_online = []                                      

    global sendOnlineThread
    sendOnlineThread = Thread(target=SendBroadcastOnlineStatus)

    recvThread.start()                                       
    sendMsgThread.start()                                    
    sendOnlineThread.start()                                 

    recvThread.join()                                         
    sendMsgThread.join()                                     
    sendOnlineThread.join()                                    

if __name__ == '__main__':
    main()
