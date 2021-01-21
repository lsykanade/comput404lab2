import socket
import time
import sys
from multiprocessing import Process

#get host information
def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#send data to server
def send_data(serversocket, payload):
    print("Sending payload")    
    try:
        serversocket.sendall(payload.encode())
    except socket.error:
        print ('Send failed')
        sys.exit()
    print("Payload sent successfully")


#define address & buffer size
HOST = "www.google.com"
port_start = 8001
port_end = 80
BUFFER_SIZE = 1024
buffer_size = 4096

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as start:
    
        #QUESTION 3
        start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        host = '127.0.0.1'

        #bind socket to address
        start.bind((host, port_start))
        #set to listening mode
        start.listen(10)
        
        #continuously listen for connections
        while True:
            conn, addr = start.accept()
            print("Connected by", addr)
            
            process = Process(target=handler, args=(conn, addr))
            process.daemon = True
            process.start()
            print("This is ", process)
            conn.close()
        start.close()

def handler(conn, addr):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as end:
                remote_ip = get_remote_ip(HOST)

                end.connect((remote_ip, port_end))
                full_data = conn.recv(BUFFER_SIZE)
                print("Data from client: ", full_data)
                time.sleep(0.5)
                end.sendall(full_data)
                end.shutdown(socket.SHUT_WR)

                full_data = b""
                while True:
                    data = end.recv(buffer_size)
                    if not data:
                        break
                    full_data += data
                #print(full_data)

                conn.sendall(full_data)
                
                print("Done!")
                end.close()
        
if __name__ == "__main__":
    main()
