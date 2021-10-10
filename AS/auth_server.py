from socket import *

serverPort = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM) 
serverSocket.bind(('', serverPort))
TTL = 1
print("This server is ready to receive")

def reg_host(recv_message):
    print(recv_message)
    recv_hostname = recv_message[1].split(':')[1]
    recv_ip = recv_message[2].split(':')[1]
    f = open('hosts.txt','a',encoding='utf-8')
    f.write(f'{recv_hostname},{recv_ip}\n')
    return f'host: {recv_hostname} has mapped to ip address {recv_ip}'

def query_address(recv_message):
    hosts_file = open('hosts.txt','r',encoding='utf-8')
    lines = hosts_file.readlines()
    recv_hostname = recv_message[1].split('=')[1]
    recv_type = recv_message[0].split('=')[1]
    for line in lines:
        host_map = line.split(',')
        if host_map[0] == recv_hostname:
            return f'TYPE={recv_type}\nNAME={recv_hostname}\nVALUE={host_map[1].strip()}\nTTL={10}'

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    recv_message = message.decode().split()
    if len(recv_message) == 4: 
        sendback = reg_host(recv_message)
        print(sendback)
    elif len(recv_message) == 2:
        sendback = query_address(recv_message)
        print(sendback)
    else:
        break
    serverSocket.sendto(sendback.encode(),clientAddress)