import socket
from GameRoom import GameRoom
import threading

class TicTacToeServer:
    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(10) #allows multiple clients to connect

        self.waiting_player = None #keep track of waiting players

    def handle_client(self, client_socket):
        if self.waiting_player:
            print("Pairing players to start a game...")
            game_room = GameRoom(self.waiting_player, client_socket)
            threading.Thread(target=game_room.handle_game).start()
            

            self.waiting_player = None

        else:
            print("Waiting for another player to join...")
            self.waiting_player = client_socket

    def start(self):
        print("Server is running and waiting for players...")

        while True:
            client_socket, address = self.server_socket.accept()

            print(f"Player connected form address {address}")

            threading.Thread(target=self.handle_client, args=(client_socket)).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()