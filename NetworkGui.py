import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from TicTacToeClient import TicTacToeClient
from cypher import generate_keys, encrypt, decrypt

class NetworkTicTacToeGUI:
    def __init__(self, root, server_ip):
        self.root = root
        self.root.title("Tic Tac Toe (Network)")
        self.buttons = []
        self.my_turn = False
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((server_ip, 12345))

        # Generate key pair
        self.private_key, self.public_key = generate_keys()
        self.client_socket.send(self.public_key)
        self.server_public_key = self.client_socket.recv(4096)

        self.create_widgets()
        threading.Thread(target=self.listen_to_server, daemon=True).start()

    def create_widgets(self):
        for i in range(9):
            btn = tk.Button(self.root, text="", width=10, height=4,
                            command=lambda i=i: self.send_move(i), font=("Arial", 24))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)

    def send_move(self, idx):
        if self.my_turn and self.buttons[idx]['text'] == "":
            self.client_socket.send(bytes(encrypt(str(idx+1), self.server_public_key), "utf-8"))
            self.my_turn = False

    def listen_to_server(self):
        game_over = False
        while True:
            try:
                data = self.client_socket.recv(4096).decode()
                if not data:
                    if game_over:
                        break
                    continue
                data = decrypt(data, self.private_key)
                if ("Wins" in data or "draw" in data or "Draw" in data) and not game_over:
                    game_over = True
                self.root.after(0, self.update_board, data)
            except Exception:
                break

    def update_board(self, data):
        # Parse board state from server message
        lines = data.strip().split('\n')
        board = []
        result_message = None
        for line in lines:
            if "|" in line:
                board.extend([cell.strip() for cell in line.split("|")])
            elif "Wins" in line or "draw" in line or "Draw" in line:
                result_message = line.strip()
        # Update buttons
        if len(board) == 9:
            for i in range(9):
                if board[i] in ["x", "o"]:
                    self.buttons[i].config(text=board[i].upper())
                else:
                    self.buttons[i].config(text="")
        # Check for turn or game over
        if "Your Move" in data:
            self.my_turn = True
        else:
            self.my_turn = False
        if result_message:
            messagebox.showinfo("Game Over", result_message)
            self.root.destroy()

    def reset_board(self):
        # Clear the buttons
        for btn in self.buttons:
            btn.config(text="")
        self.my_turn = False
        # Optionally, reconnect to the server for a new game
        # Or, you can close and reopen the window, or prompt for replay
        # For now, just wait for the server to pair you again

if __name__ == "__main__":
    root = tk.Tk()
    server_ip = simpledialog.askstring("Server IP", "Enter server IP address:", parent=root)
    if server_ip:
        app = NetworkTicTacToeGUI(root, server_ip)
        root.mainloop()