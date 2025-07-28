import tkinter as tk
import random

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Tic Tac Toe")
        self.window.resizable(False, False)

        self.player = "X"
        self.ai = "O"
        self.board = [""] * 9
        self.buttons = []

        self.status_label = tk.Label(self.window, text="Your turn (X)", font=("Segoe UI", 16), bg="#121212", fg="#00e676")
        self.status_label.pack(fill="x")

        self.frame = tk.Frame(self.window, bg="#121212")
        self.frame.pack()

        for i in range(9):
            btn = tk.Button(
                self.frame,
                text="",
                width=6,
                height=3,
                font=("Segoe UI", 24),
                command=lambda i=i: self.player_move(i),
                bg="#1f1f1f",
                fg="white"
            )
            btn.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(btn)

        self.reset_button = tk.Button(self.window, text="Reset", command=self.reset_game, bg="#00e676", fg="black")
        self.reset_button.pack(pady=10)

    def player_move(self, index):
        if self.board[index] == "" and not self.check_winner():
            self.make_move(index, self.player)
            if not self.check_winner() and "" in self.board:
                self.window.after(500, self.ai_move)

    def ai_move(self):
        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.ai
                if self.check_winner() == self.ai:
                    self.make_move(i, self.ai)
                    return
                self.board[i] = ""

        for i in range(9):
            if self.board[i] == "":
                self.board[i] = self.player
                if self.check_winner() == self.player:
                    self.board[i] = ""
                    self.make_move(i, self.ai)
                    return
                self.board[i] = ""

        empty = [i for i, v in enumerate(self.board) if v == ""]
        if empty:
            i = random.choice(empty)
            self.make_move(i, self.ai)

    def make_move(self, index, player):
        self.board[index] = player
        self.buttons[index].config(text=player, state="disabled")
        winner = self.check_winner()
        if winner:
            self.status_label.config(text=f"{'You win!' if winner == self.player else 'AI wins!'}")
        elif "" not in self.board:
            self.status_label.config(text="It's a draw!")
        else:
            self.status_label.config(text=f"{'Your' if player == self.ai else 'AI'} turn")

    def check_winner(self):
        combos = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for a, b, c in combos:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                for i in (a, b, c):
                    self.buttons[i].config(bg="#00e676")
                return self.board[a]
        return None

    def reset_game(self):
        self.board = [""] * 9
        self.status_label.config(text="Your turn (X)")
        for btn in self.buttons:
            btn.config(text="", state="normal", bg="#1f1f1f")

def launch_game():
    TicTacToeGame()


