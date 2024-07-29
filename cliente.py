import socket
import threading
import pickle

class ChatClient:
    def __init__(self, router_port):
        self.router_address = ('localhost', router_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, dest, message):
        data = {'type': 'chat', 'dest': dest, 'data': message}
        self.socket.sendto(pickle.dumps(data), self.router_address)

    def receive_messages(self):
        while True:
            message, addr = self.socket.recvfrom(4096)
            message = pickle.loads(message)
            print(f"Message received: {message['data']}")

    def start(self):
        threading.Thread(target=self.receive_messages).start()
        while True:
            dest = input("Enter destination router ID: ")
            message = input("Enter message: ")
            self.send_message(dest, message)

if __name__ == "__main__":
    router_port = int(input("Enter your router port: "))
    client = ChatClient(router_port)
    client.start()
