# Network Tic Tac Toe

A Python-based network Tic Tac Toe game supporting multiple simultaneous games, with a graphical interface for both players. All communication is encrypted using AES Encryption.

---

## Features

- Play Tic Tac Toe over a network (LAN or internet)
- GUI for both players (Tkinter)
- Multiple games can run at the same time (multi-room support)
- All communication is encrypted with a Caesar cipher
- Simple, modular codebase

---

## Requirements

- Python 3.x
- Tkinter (usually included with Python)
- All project files in the same directory:
  - `NetworkGui.py`
  - `TicTacToeClient.py`
  - `TicTacToeServer.py`
  - `GameRoom.py`
  - `Board.py`
  - `cypher.py`
  - `Cryptography` module python (`pip install cryptography`)

---

## How to Run

### 1. Start the Server

On one computer (the server):

```sh
python3 TicTacToeServer.py
```

### 2. Find the Server's IP Address

On the server, run:

```sh
hostname -I
```

Note the IP address (e.g., `192.168.1.100`).

### 3. Start the GUI Client

On both computers (players):

```sh
python3 NetworkGui.py
```

When prompted, enter the server's IP address.

---

## How to Play

- Each player gets a 3x3 grid.
- Click a cell to make your move when it's your turn.
- The board updates automatically.
- The game ends when someone wins or it's a draw.

---

## Encryption

All messages between client and server are encrypted using a Caesar cipher (see `cypher.py`).

---

## Troubleshooting

- Make sure both computers are on the same network.
- Ensure port `12345` is open on the server.
- If you get connection errors, check your firewall settings.

---

## License

ministry of education
---

## Credits

- Developed by Moshe Bekritsky
