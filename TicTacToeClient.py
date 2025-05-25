import socket
from cypher import generate_keys, encrypt, decrypt

class TicTacToeClient:
    def __init__(self, server_ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, 12345))

        # Generate key pair
        self.private_key, self.public_key = generate_keys()

        # Exchange public keys
        # Send our public key
        self.client_socket.send(self.public_key)
        # Receive server's public key
        self.server_public_key = self.client_socket.recv(4096)

    def start(self):
        while True:
            # Receive and decrypt message using our private key
            board_state = decrypt(self.client_socket.recv(4096).decode(), self.private_key)
            print(board_state)

            if "wins" in board_state or "draw" in board_state:
                break

            move = input("Enter your move (1-9): ")
            # Encrypt move with server's public key
            self.client_socket.send(bytes(encrypt(move, self.server_public_key), "utf-8"))


