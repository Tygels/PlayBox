import tkinter as tk
import random

CELL_SIZE = 30
COLUMNS = 10
ROWS = 20
SPEED = 500  # milliseconds

SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0], [1, 1, 1]],
    'L': [[0, 0, 1], [1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'Z': [[1, 1, 0], [0, 1, 1]],
}

COLORS = {
    'I': '#00f0f0',
    'J': '#0000f0',
    'L': '#f0a000',
    'O': '#f0f000',
    'S': '#00f000',
    'T': '#a000f0',
    'Z': '#f00000',
}

class TetrisGame:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Tetris")
        self.canvas = tk.Canvas(self.window, width=CELL_SIZE*COLUMNS, height=CELL_SIZE*ROWS, bg="#121212")
        self.canvas.pack()
        self.window.bind("<Key>", self.handle_key)

        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.running = True
        self.current = None
        self.current_pos = (0, 3)

        self.spawn_piece()
        self.game_loop()

    def spawn_piece(self):
        self.shape_type = random.choice(list(SHAPES.keys()))
        self.shape = SHAPES[self.shape_type]
        self.color = COLORS[self.shape_type]
        self.current_pos = (0, COLUMNS // 2 - len(self.shape[0]) // 2)
        if self.check_collision(self.current_pos, self.shape):
            self.game_over()

    def rotate(self):
        return [list(row) for row in zip(*self.shape[::-1])]

    def check_collision(self, pos, shape):
        row, col = pos
        for r in range(len(shape)):
            for c in range(len(shape[0])):
                if shape[r][c]:
                    nr = row + r
                    nc = col + c
                    if nr < 0 or nr >= ROWS or nc < 0 or nc >= COLUMNS or self.board[nr][nc]:
                        return True
        return False

    def lock_piece(self):
        row, col = self.current_pos
        for r in range(len(self.shape)):
            for c in range(len(self.shape[0])):
                if self.shape[r][c]:
                    self.board[row + r][col + c] = self.color
        self.clear_lines()
        self.spawn_piece()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell is None for cell in row)]
        cleared = ROWS - len(new_board)
        for _ in range(cleared):
            new_board.insert(0, [None for _ in range(COLUMNS)])
        self.board = new_board

    def move(self, drow, dcol):
        new_pos = (self.current_pos[0] + drow, self.current_pos[1] + dcol)
        if not self.check_collision(new_pos, self.shape):
            self.current_pos = new_pos
            return True
        return False

    def drop(self):
        if not self.move(1, 0):
            self.lock_piece()

    def handle_key(self, event):
        if not self.running:
            return
        if event.keysym == 'Left':
            self.move(0, -1)
        elif event.keysym == 'Right':
            self.move(0, 1)
        elif event.keysym == 'Down':
            self.drop()
        elif event.keysym == 'Up':
            rotated = self.rotate()
            if not self.check_collision(self.current_pos, rotated):
                self.shape = rotated

    def draw_board(self):
        self.canvas.delete("all")

        # Draw existing blocks
        for r in range(ROWS):
            for c in range(COLUMNS):
                color = self.board[r][c]
                if color:
                    self.draw_cell(r, c, color)

        # Draw falling block
        row, col = self.current_pos
        for r in range(len(self.shape)):
            for c in range(len(self.shape[0])):
                if self.shape[r][c]:
                    self.draw_cell(row + r, col + c, self.color)

    def draw_cell(self, row, col, color):
        x1 = col * CELL_SIZE
        y1 = row * CELL_SIZE
        x2 = x1 + CELL_SIZE
        y2 = y1 + CELL_SIZE
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#121212")

    def game_over(self):
        self.running = False
        self.canvas.create_text(CELL_SIZE*COLUMNS//2, CELL_SIZE*ROWS//2, text="Game Over", fill="white", font=("Segoe UI", 24))
        btn = tk.Button(self.window, text="Try Again", command=self.restart, bg="#00e676", fg="black")
        self.canvas.create_window(CELL_SIZE*COLUMNS//2, CELL_SIZE*ROWS//2 + 40, window=btn)

    def restart(self):
        self.board = [[None for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.running = True
        self.spawn_piece()
        self.game_loop()

    def game_loop(self):
        if self.running:
            self.drop()
            self.draw_board()
            self.window.after(SPEED, self.game_loop)

def launch_game():
    TetrisGame()

