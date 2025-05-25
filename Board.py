class Board:
    def __init__(self):
        self.board = ["1","2","3","4","5","6","7","8","9"]

    def display(self):
        return (
            f"\n{self.board[0]} | {self.board[1]} | {self.board[2]}"
            f"\n--+---+--"
            f"\n{self.board[3]} | {self.board[4]} | {self.board[5]}"
            f"\n--+---+--"
            f"\n{self.board[6]} | {self.board[7]} | {self.board[8]}"
        )
    
    def update(self, position, marker):
        self.board[position] = marker

    def is_winner(self, marker):
        winning_combinations = [[0,1,2], [3,4,5],
                                [6,7,8], [0,3,6],
                                [1,4,7], [2,5,8],
                                [0,4,8], [2,4,6]]
        
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] == marker:
                return True
            
        return False
    
    def is_draw(self):
        return all(spot in ["x", "o"] for spot in self.board)