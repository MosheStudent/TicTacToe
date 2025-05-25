from Board import Board
from cypher import generate_keys, encrypt, decrypt
import datetime

class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "x"), (player2_socket, "o")]
        self.current_player = 0

        # Server key pair
        self.server_private_key, self.server_public_key = generate_keys()

        # Receive public keys from both players
        self.player_public_keys = []
        for player_socket, _ in self.players:
            pubkey = player_socket.recv(4096)
            self.player_public_keys.append(pubkey)
        # Send server's public key to both players
        for player_socket, _ in self.players:
            player_socket.send(self.server_public_key)

    def send_board_to_players(self):
        board_state = self.board.display()
        for idx, (player_socket, _) in enumerate(self.players):
            player_socket.send(bytes(encrypt(board_state, self.player_public_keys[idx]), "utf-8"))

    def handle_game(self):
        game_over = False
        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            self.send_board_to_players()
            current_socket.send(bytes(encrypt("Your Move:", self.player_public_keys[self.current_player]), "utf-8"))
            move = decrypt(current_socket.recv(4096).decode("utf-8"), self.server_private_key)
            try:
                move = int(move) - 1
                if self.board.board[move] not in ["x", "o"]:
                    self.board.update(move, current_marker)
                else:
                    continue
            except Exception:
                continue
            if self.board.is_winner(current_marker):
                msg = f"Player {current_marker.upper()} Wins!"
                for idx, (player_socket, _) in enumerate(self.players):
                    player_socket.send(bytes(encrypt(msg, self.player_public_keys[idx]), "utf-8"))
                game_over = True
            elif self.board.is_draw():
                msg = "It's a draw!"
                for idx, (player_socket, _) in enumerate(self.players):
                    player_socket.send(bytes(encrypt(msg, self.player_public_keys[idx]), "utf-8"))
                game_over = True
            else:
                self.current_player = (self.current_player + 1) % 2
        # Log game
        try:
            log_game(self.players[0][0].getpeername()[0], self.players[1][0].getpeername()[0])
        except Exception as e:
            print(f"Error logging game: {e}")

def log_game(player1_addr, player2_addr):
    with open("games_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} - {player1_addr} vs {player2_addr}\n")
