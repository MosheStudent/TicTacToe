def send_board_to_players(self):
    board_state = self.board.display()
    # Send "Your Move" message only to the current player, but always include latest board for both
    for i, (player_socket, _) in enumerate(self.players):
        if i == self.current_player:
            msg = board_state + "\nYour Move:"
        else:
            msg = board_state
        player_socket.send(encrypt(msg))

def handle_game(self):
    game_over = False

    while not game_over:
        current_socket, current_marker = self.players[self.current_player]

        self.send_board_to_players()

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