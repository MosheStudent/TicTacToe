from Board import Board
from cypher import encrypt, decrypt
from datetime import datetime
import os

class GameRoom:
    def __init__(self, player1_socket, player2_socket):
        self.board = Board()
        self.players = [(player1_socket, "x"), (player2_socket, "o")]   
        self.current_player = 0

    def send_board_to_players(self):
        board_state = self.board.display()

        for player_socket, _ in self.players:
            player_socket.send(encrypt(board_state))

    def handle_game(self):
        game_over = False

        while not game_over:
            current_socket, current_marker = self.players[self.current_player]
            opponent_socket, _ = self.players[(self.current_player + 1) % 2]

            self.send_board_to_players()
            current_socket.send(encrypt("Your Move: "))
            move = decrypt(current_socket.recv(1024))

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
                    player_socket.send(encrypt(self.board.display() + "\n" + msg))
                game_over = True
                self.save_game_result(msg)
            elif self.board.is_draw():
                msg = "It's a draw!"
                for player_socket, _ in self.players:
                    player_socket.send(encrypt(self.board.display() + "\n" + msg))
                game_over = True
                self.save_game_result(msg)
            else:
                self.current_player = (self.current_player + 1) % 2

        # Optionally, close sockets here if you want to end the session

    def save_game_result(self, result):
        # Get current time
        game_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Get player IP addresses
        player1_ip = self.players[0][0].getpeername()[0]
        player2_ip = self.players[1][0].getpeername()[0]
        
        # Get final board state
        board_state = self.board.display()
        
        # Prepare log entry
        log_entry = (
            f"Game Time: {game_time}\n"
            f"Player X IP: {player1_ip}\n"
            f"Player O IP: {player2_ip}\n"
            f"Result: {result}\n"
            f"Final Board:\n{board_state}\n"
            f"{'-' * 50}\n"
        )
        
        # Append to log file
        with open("game_log.txt", "a") as f:
            f.write(log_entry)