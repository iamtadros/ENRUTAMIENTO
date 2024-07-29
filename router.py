import socket
import threading
import pickle

class Router:
    def __init__(self, router_id, port, neighbors):
        self.router_id = router_id
        self.port = port
        self.neighbors = neighbors
        self.routing_table = {router_id: (0, router_id)}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('localhost', port))
        threading.Thread(target=self.listen).start()

    def listen(self):
        while True:
            message, addr = self.socket.recvfrom(4096)
            message = pickle.loads(message)
            if message['type'] == 'update':
                self.update_routing_table(message['router_id'], message['table'])
            elif message['type'] == 'chat':
                self.route_message(message['dest'], message['data'])

    def update_routing_table(self, neighbor_id, neighbor_table):
        updated = False
        for dest, (cost, next_hop) in neighbor_table.items():
            if dest not in self.routing_table or self.routing_table[dest][0] > cost + 1:
                self.routing_table[dest] = (cost + 1, neighbor_id)
                updated = True
        if updated:
            self.broadcast_table()

    def broadcast_table(self):
        message = {'type': 'update', 'router_id': self.router_id, 'table': self.routing_table}
        for neighbor in self.neighbors:
            self.socket.sendto(pickle.dumps(message), ('localhost', neighbor))

    def route_message(self, dest, data):
        if dest in self.routing_table:
            next_hop = self.routing_table[dest][1]
            if next_hop == self.router_id:
                print(f"Message received at {self.router_id}: {data}")
            else:
                self.socket.sendto(pickle.dumps({'type': 'chat', 'dest': dest, 'data': data}), ('localhost', next_hop))

    def send_message(self, dest, data):
        self.route_message(dest, data)

    def start(self):
        self.broadcast_table()
