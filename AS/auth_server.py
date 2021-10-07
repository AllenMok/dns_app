from socket import *

serverPort = 53533
serverSocket = socket(AF_INET, SOCK_DGRAM) 
serverSocket.bind(('', serverPort)) 
print("This server is ready to receive")

def reg_host(rev_message):
    print(rev_message)
    rev_hostname = rev_message[1].split(':')[1]
    rev_ip = rev_message[2].split(':')[1]
    f = open('hosts.txt','a',encoding='utf-8')
    f.write(f'{rev_hostname},{rev_ip}\n')
    return f'host: {rev_hostname} has mapped to ip address {rev_ip}'

def query_address(rev_message):
    hosts_file = open('hosts.txt','r',encoding='utf-8')
    lines = hosts_file.readlines()
    rev_hostname = rev_message[1].split('=')[1]
    rev_type = rev_message[0].split('=')[1]
    for line in lines:
        host_map = line.split(',')
        if host_map[0] == rev_hostname:
            return f'TYPE={rev_type}\nNAME={rev_hostname}\nVALUE={host_map[1]}\nTTL={10}'

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    rev_message = message.decode().split()
    if len(rev_message) == 4: 
        sendback = reg_host(rev_message)
        print(sendback)
    elif len(rev_message) == 2:
        sendback = query_address(rev_message)
        print(sendback)
    else:
        break
    serverSocket.sendto(sendback.encode(),clientAddress)