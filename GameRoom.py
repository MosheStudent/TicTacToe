from Board import Board
from cypher import generate_keys, encrypt, decrypt
import datetime

class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "x"), (player2_socket, "o")]
        self.current_player = 0

        # Server generates its own key pair
        self.server_private_key, self.server_public_key = generate_keys()

        # Receive public keys from both players
        self.player_public_keys = []
        for player_socket, _ in self.players:
            try:
                pubkey = player_socket.recv(4096)
                if not pubkey:
                    raise ConnectionError("Player disconnected during key exchange.")
                self.player_public_keys.append(pubkey)
            except Exception as e:
                print(f"Error receiving public key: {e}")
                self.close_all()
                return

        # Send server's public key to both players
        for player_socket, _ in self.players:
            try:
                player_socket.send(self.server_public_key)
            except Exception as e:
                print(f"Error sending server public key: {e}")
                self.close_all()
                return

    def send_board_to_players(self):
        board_state = self.board.display()
        for idx, (player_socket, _) in enumerate(self.players):
            try:
                player_socket.send(bytes(encrypt(board_state, self.player_public_keys[idx]), "utf-8"))
            except Exception as e:
                print(f"Error sending board to player {idx}: {e}")

    def handle_game(self):
        game_over = False

        while not game_over:
            try:
                current_socket, current_marker = self.players[self.current_player]
                opponent_socket, _ = self.players[(self.current_player + 1) % 2]

                self.send_board_to_players()
                # Only send "Your Move" to the current player
                current_socket.send(bytes(encrypt("Your Move:", self.player_public_keys[self.current_player]), "utf-8"))

                # Receive and decrypt move
                try:
                    move_data = current_socket.recv(4096)
                    if not move_data:
                        print("Player disconnected during move.")
                        break
                    move = decrypt(move_data.decode("utf-8"), self.server_private_key)
                except Exception as e:
                    print(f"Error receiving/decrypting move: {e}")
                    break

                # Validate move
                try:
                    move = int(move) - 1
                    if self.board.board[move] not in ["x", "o"]:
                        self.board.update(move, current_marker)
                    else:
                        continue  # Invalid move, ask again
                except Exception:
                    continue  # Invalid input, ask again

                # Check for win/draw
                if self.board.is_winner(current_marker):
                    msg = f"Player {current_marker.upper()} Wins!"
                    for idx, (player_socket, _) in enumerate(self.players):
                        try:
                            player_socket.send(bytes(encrypt(msg, self.player_public_keys[idx]), "utf-8"))
                        except Exception as e:
                            print(f"Error sending win message: {e}")
                    game_over = True
                elif self.board.is_draw():
                    msg = "It's a draw!"
                    for idx, (player_socket, _) in enumerate(self.players):
                        try:
                            player_socket.send(bytes(encrypt(msg, self.player_public_keys[idx]), "utf-8"))
                        except Exception as e:
                            print(f"Error sending draw message: {e}")
                    game_over = True
                else:
                    self.current_player = (self.current_player + 1) % 2

            except Exception as e:
                print(f"Unexpected error in game loop: {e}")
                break

        # Log the game result
        try:
            self.log_game(self.players[0][0].getpeername()[0], self.players[1][0].getpeername()[0])
        except Exception as e:
            print(f"Error logging game: {e}")

        self.close_all()

    def log_game(self, player1_addr, player2_addr):
        with open("games_log.txt", "a") as f:
            f.write(f"{datetime.datetime.now()} - {player1_addr} vs {player2_addr}\n")

    def close_all(self):
        for player_socket, _ in self.players:
            try:
                player_socket.close()
            except Exception:
                pass
