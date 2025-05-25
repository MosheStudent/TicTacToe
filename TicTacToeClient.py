import socket
from cypher import encrypt, decrypt

def recv_message(sock):
    buffer = b""
    while not buffer.endswith(b"\n"):
        part = sock.recv(1024)
        if not part:
            raise ConnectionError("Socket closed")
        buffer += part
    return decrypt(buffer.strip().decode("utf-8"))

class TicTacToeClient:
    def __init__(self, server_ip):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, 12345))

    def start(self):
        while True:
            board_state = recv_message(self.client_socket)
            print(board_state)

            if "wins" in board_state.lower() or "draw" in board_state.lower():
                break

            move = input("Enter your move (1-9): ")
            self.client_socket.send((encrypt(move) + "\n").encode("utf-8"))
