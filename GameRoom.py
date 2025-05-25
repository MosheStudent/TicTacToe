from Board import Board
from cypher import encrypt, decrypt


class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "x"), (player2_socket, "o")]   
        self.current_player = 0

    def send_board_to_players(self):
        board_state = self.board.display()

        for player_socket, _ in self.players:
            player_socket.send(bytes(encrypt(board_state), "utf-8"))

    def handle_game(self):
        game_over = False

        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            opponent_socket, _ = self.players[(self.current_player + 1) % 2]

            self.send_board_to_players()
            current_socket.send(bytes(encrypt("Your Move: "), "utf-8"))
            move = decrypt(current_socket.recv(1024).decode("utf-8"))

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
                for player_socket, _ in self.players:
                    player_socket.send(bytes(encrypt(self.board.display() + "\n" + msg), "utf-8"))
                game_over = True
            elif self.board.is_draw():
                msg = "It's a draw!"
                for player_socket, _ in self.players:
                    player_socket.send(bytes(encrypt(self.board.display() + "\n" + msg), "utf-8"))
                game_over = True
            else:
                self.current_player = (self.current_player + 1) % 2

        # Optionally, close sockets here if you want to end the session

        with open("game_log.txt", "a") as log_file:
            log_file.write(self.board.display() + "\n")
            if game_over:
                log_file.write(msg + "\n")
            log_file.write("-" * 20 + "\n")
        print("Game over. Log saved to game_log.txt")
            
