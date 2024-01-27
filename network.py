import socket
import pickle

class Network:
    def __init__(self) :
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.68.100" # My IP
        self.port = 4444
        self.addr = (self.server,self.port)
        self.p = self.Connect()

    def GetP(self):
        return self.p

    def Connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    def Send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(1024))
        except socket.error as e:
            print(e)

