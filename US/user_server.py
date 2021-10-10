from flask import Flask, request, make_response
import requests
from socket import *
import json

app = Flask(__name__)

def query_ip(as_ip, as_port, query_info, TTL=10):
    serverName = as_ip
    serverPort = int(as_port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    clientSocket.settimeout(TTL)
    message = query_info
    clientSocket.sendto(message.encode(), (serverName, serverPort))
    resp_message, serverAddress = clientSocket.recvfrom(2048)
    resp_message = resp_message.decode()
    clientSocket.close()
    return resp_message


@app.route('/fibonacci')
def fib():
    try:
        hostname = request.args.get('hostname')
        fs_port = request.args.get('fs_port')
        num = request.args.get('number')
        as_ip = request.args.get('as_ip')
        as_port = request.args.get('as_port')
        for i in [hostname, fs_port, num, as_ip, as_port]:
            if i == '':
                raise ValueError
    except:
        return 'HTTP_400_BAD_REQUEST', 400
    dns_type = 'A'
    query_info = f'TYPE={dns_type}\nNAME={hostname}'
    try:
        fs_info = query_ip(as_ip, as_port, query_info)
    except:
        return 'HTTP_404_NOT_FOUND', 404
    fs_ip_resp = fs_info.split()[2][6:]
    try:
        url = f'http://{fs_ip_resp}:{fs_port}/fibonacci?number={num}'
        fib_resp = requests.get(url)
    except:
        return 'HTTP_404_NOT_FOUND', 404
    return fib_resp.text, 200


app.run(host='0.0.0.0',
        port=8080,
        debug=True)
