from flask import Flask, request, make_response, jsonify
import requests
from socket import *
import json

app = Flask(__name__)

def reg_udp(as_ip,as_port,register_message):
    serverName = as_ip
    serverPort = int(as_port)
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = register_message
    clientSocket.sendto(message.encode(),(serverName, serverPort)) 
    resp_message, serverAddress = clientSocket.recvfrom(2048) 
    app.logger.info(resp_message.decode())
    clientSocket.close()
    return resp_message

@app.route('/register', methods = ['PUT'])
def register():
    hostname = request.json['hostname']
    register_ip = request.json['ip']
    as_ip = request.json['as_ip']
    as_port = request.json['as_port']
    dns_type = 'A'
    resp_message = reg_udp(as_ip,as_port,f'TYPE:{dns_type}\nNAME:{hostname}\nVALUE:{register_ip}\nTTL:10')
    app.logger.info(resp_message)
    resp = make_response(resp_message)
    app.logger.info(resp)
    return resp,201

@app.route('/fibonacci')
def fib_num():
    try:
        seq = int(request.args.get('number'))
        assert(seq>=1) 
    except:
        return 'Bad Format', 400
    fib = Fibonacci()
    fib_num = fib.sequence(seq)
    resp = make_response(str(fib_num))
    return resp, 200

class Fibonacci(object):

    def __init__(self):
        self._results = [0, 1]

    def __compute(self, n):
        for i in range(len(self._results), n):
            self._results.append(self._results[i-1] + self._results[i-2])

    def sequence(self, n):
        self.__compute(n)
        return self._results[n-1]

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
