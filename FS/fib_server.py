from flask import Flask, request, make_response, jsonify
import requests
from socket import *
import json

app = Flask(__name__)

@app.route('/register', method = ['PUT'])
# def register():
#     hostname = request.json['hostname']
#     local_ip = request.json['ip']
#     as_ip = request.json['as_ip']
#     as_port = request.json['as_port']
#     reg_udp(as_ip,as_port,f'TYPE:A\nNAME:{hostname}\nVALUE:{ip}\nTTL:10')

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

def reg_udp(as_ip,as_port,message):
    serverName = as_ip
    serverPort = as_port
    clientSocket = socket(AF_INET, SOCK_DGRAM)
    message = mess
    clientSocket.sendto(message.encode(),(serverName, serverPort)) 
    modifiedMessage, serverAddress = clientSocket.recvfrom(2048) 
    print(modifiedMessage.decode())
    clientSocket.close()

app.run(host='0.0.0.0',
        port=9090,
        debug=True)
