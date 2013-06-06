import socket
import json
import threading

class Reciever(threading.Thread):

    initials = []
    counters = {}

    IP = "127.0.0.1"
    PORT = 38519
    socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socket.bind((IP, PORT))

    def run(self):
        while True:
            data, addr = self.socket.recvfrom(1024)
            data = json.loads(data)
            if data['name'] in self.counters:
                self.counters[data['name']] += 1
            else:
                self.counters[data['name']] = 1
                self.initials.append(data['name'])

    def get_counters(self):
        counters = []
        for name, value in self.counters.items():
            # Because a new librato-run starts at 0, ensure that the first transmission always starts with 0
            if name in self.initials:
                value = 0
            counters.append({
                'name': name,
                'value': value
            })
            self.initials = []
        return counters
