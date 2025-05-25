import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
from TicTacToeClient import TicTacToeClient

class NetworkTicTacToeGUI:
    def __init__(self, root, server_ip):
        self.root = root
        self.root.title("Tic Tac Toe (Network)")
        self.buttons = []
        self.my_turn = False
        try:
            self.client = TicTacToeClient(server_ip)
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            root.destroy()
            return
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
            try:
                self.client.send(str(idx+1))
                self.my_turn = False
            except Exception as e:
                messagebox.showerror("Send Error", str(e))
                self.root.destroy()

    def listen_to_server(self):
        game_over = False
        while True:
            try:
                data = self.client.receive()
                if not data:
                    if game_over:
                        break
                    continue
                if ("Wins" in data or "draw" in data or "Draw" in data) and not game_over:
                    game_over = True
                self.root.after(0, self.update_board, data)
            except Exception:
                break

    def update_board(self, data):
        lines = data.strip().split('\n')
        board = []
        result_message = None
        for line in lines:
            if "|" in line:
                board.extend([cell.strip() for cell in line.split("|")])
            elif "Wins" in line or "draw" in line or "Draw" in line:
                result_message = line.strip()
        if len(board) == 9:
            for i in range(9):
                if board[i] in ["x", "o"]:
                    self.buttons[i].config(text=board[i].upper())
                else:
                    self.buttons[i].config(text="")
        if "Your Move" in data:
            self.my_turn = True
        else:
            self.my_turn = False
        if result_message:
            messagebox.showinfo("Game Over", result_message)
            self.root.destroy()

    def reset_board(self):
        for btn in self.buttons:
            btn.config(text="")
        self.my_turn = False

if __name__ == "__main__":
    root = tk.Tk()
    server_ip = simpledialog.askstring("Server IP", "Enter server IP address:", parent=root)
    if server_ip:
        try:
            app = NetworkTicTacToeGUI(root, server_ip)
            root.mainloop()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Could not connect to server:\n{e}")
            root.destroy()