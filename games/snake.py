import tkinter as tk
import random

GRID_SIZE = 20
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
SPEED = 100

class SnakeGame:
    def __init__(self):
        self.window = tk.Toplevel()
        self.window.title("Snake")
        self.window.resizable(False, False)

        self.canvas = tk.Canvas(self.window, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#1f1f1f")
        self.canvas.pack()

        self.window.bind("<KeyPress>", self.change_direction)

        self.after_id = None
        self.try_again_button = None
        self.start_button = tk.Button(
            self.window,
            text="Start Game",
            command=self.start_game,
            bg="#00e676",
            fg="#000",
            font=("Segoe UI", 14),
            relief="flat"
        )
        self.canvas.create_window(CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2, window=self.start_button)

    def start_game(self):
       
        if self.start_button:
            self.start_button.destroy()
        if self.try_again_button:
            self.try_again_button.destroy()

        
        self.snake = [(100, 100)]
        self.direction = "Right"
        self.food = self.place_food()
        self.running = True

        self.canvas.delete("all")
        self.window.focus_set()

        self.update()

    def draw_snake(self):
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="#00e676", tag="snake")

    def draw_food(self):
        x, y = self.food
        self.canvas.delete("food")
        self.canvas.create_oval(x, y, x+GRID_SIZE, y+GRID_SIZE, fill="#ff1744", tag="food")

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == "Left":
            head_x -= GRID_SIZE
        elif self.direction == "Right":
            head_x += GRID_SIZE
        elif self.direction == "Up":
            head_y -= GRID_SIZE
        elif self.direction == "Down":
            head_y += GRID_SIZE

        new_head = (head_x, head_y)

        if (
            head_x < 0 or head_x >= CANVAS_WIDTH or
            head_y < 0 or head_y >= CANVAS_HEIGHT or
            new_head in self.snake
        ):
            self.end_game()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.food = self.place_food()
        else:
            self.snake.pop()

    def place_food(self):
        while True:
            x = random.randint(0, (CANVAS_WIDTH - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            y = random.randint(0, (CANVAS_HEIGHT - GRID_SIZE) // GRID_SIZE) * GRID_SIZE
            if (x, y) not in self.snake:
                return (x, y)

    def change_direction(self, event):
        if not self.running:
            return

        key = event.keysym
        opposites = {
            "Left": "Right",
            "Right": "Left",
            "Up": "Down",
            "Down": "Up"
        }
        if key in ["Left", "Right", "Up", "Down"] and key != opposites.get(self.direction):
            self.direction = key

    def update(self):
        if self.running:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
            self.after_id = self.window.after(SPEED, self.update)

    def end_game(self):
        self.running = False
        if self.after_id:
            self.window.after_cancel(self.after_id)

        self.canvas.create_text(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 - 20,
            text="Game Over!",
            fill="white",
            font=("Segoe UI", 24)
        )

        self.try_again_button = tk.Button(
            self.window,
            text="Try Again",
            command=self.start_game,
            bg="#00e676",
            fg="#000",
            font=("Segoe UI", 12),
            relief="flat"
        )
        self.canvas.create_window(
            CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2 + 30,
            window=self.try_again_button
        )

def launch_game():
    SnakeGame()

