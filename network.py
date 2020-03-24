#network to wszystkie funkcje ze strony klienta, ktore beda komunikowac sie z
#serwerem. Mozesz tu ustalic, w jaki sposob dane beda wysylane do serwera oraz
#jakie dane beda odbierane

import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.0.23"
        self.port = 5556
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            #self.client.send(str.encode(data))
            #print("wchodze w network.send()")
            data = pickle.dumps(data)
            self.client.send(data)
            #return self.client.recv(2048).decode()
            return pickle.loads(self.client.recv(4*2048))
        except socket.error as e:
            print(e)