import socket
from cypher import encrypt, decrypt

class TicTacToeClient:
    def __init__(self, server_ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.client_socket.connect((server_ip, 12345))

    def start(self):
        while True:
            board_state = decrypt(self.client_socket.recv(1024).decode())
            print(board_state)

            if "wins" in board_state or "draw" in board_state:
                break

            move = input("Enter your move (1-9): ")
            self.client_socket.send(bytes(encrypt(move), "utf-8"))


