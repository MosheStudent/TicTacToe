import socket
from cypher import generate_keys, encrypt, decrypt

class TicTacToeClient:
    def __init__(self, server_ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, 12345))
        self.private_key, self.public_key = generate_keys()
        self.client_socket.send(self.public_key)
        self.server_public_key = self.client_socket.recv(4096)

    def send(self, text):
        self.client_socket.send(bytes(encrypt(text, self.server_public_key), "utf-8"))

    def receive(self):
        data = self.client_socket.recv(4096).decode()
        return decrypt(data, self.private_key)

    def start(self):
        while True:
            board_state = self.receive()
            print(board_state)

            if "wins" in board_state or "draw" in board_state:
                break

            move = input("Enter your move (1-9): ")
            self.send(move)


