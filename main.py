import tkinter as tk
from tkinter import messagebox
from games import snake, tictactoe, tetris

class PlayBoxApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PlayBox")
        self.root.geometry("300x400")
        self.root.configure(bg="#121212")

        title = tk.Label(root, text="Playbox", font=("Segoe UI", 24), fg="#00e676", bg="#121212")
        title.pack(pady=30)

        btn_snake = tk.Button(root, text="Play Snake", command=snake.launch_game, width=20, height=2, bg="#1f1f1f", fg="white")
        btn_snake.pack(pady=10)

        btn_ttt = tk.Button(root, text="Play Tic Tac Toe", command=tictactoe.launch_game, width=20, height=2, bg="#1f1f1f", fg="white")
        btn_ttt.pack(pady=10)

        btn_tetris = tk.Button(root, text="Play Tetris", command=tetris.launch_game, width=20, height=2, bg="#1f1f1f", fg="white")
        btn_tetris.pack(pady=10)

        quit_btn = tk.Button(root, text="Exit", command=root.quit, width=10, bg="#ff1744", fg="white")
        quit_btn.pack(side="bottom", pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlayBoxApp(root)
    root.mainloop()
