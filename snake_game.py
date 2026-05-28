"""Snake Game - Data Collection Learning Project

A simple snake game to practice Python programming.
"""

import random
import tkinter as tk
from tkinter import font as tkfont

CELL_SIZE = 20
GRID_WIDTH = 25
GRID_HEIGHT = 20
CANVAS_WIDTH = CELL_SIZE * GRID_WIDTH
CANVAS_HEIGHT = CELL_SIZE * GRID_HEIGHT


class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("贪吃蛇")
        self.window.resizable(False, False)

        self.title_font = tkfont.Font(family="Helvetica", size=24, weight="bold")
        self.button_font = tkfont.Font(family="Helvetica", size=14)
        self.score_font = tkfont.Font(family="Helvetica", size=16)

        self.main_frame = tk.Frame(self.window, bg="#1a1a2e")
        self.main_frame.pack()

        self.title_label = tk.Label(
            self.main_frame, text="贪吃蛇", font=self.title_font, fg="#eee", bg="#1a1a2e"
        )
        self.title_label.pack(pady=20)

        self.score_label = tk.Label(
            self.main_frame, text="分数: 0", font=self.score_font, fg="#4ecca3", bg="#1a1a2e"
        )
        self.score_label.pack()

        self.canvas = tk.Canvas(
            self.main_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="#16213e",
            highlightthickness=0,
        )
        self.canvas.pack(pady=20)

        self.button_frame = tk.Frame(self.main_frame, bg="#1a1a2e")
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame,
            text="开始游戏",
            font=self.button_font,
            fg="#fff",
            bg="#4ecca3",
            activebackground="#3db892",
            activeforeground="#fff",
            relief="flat",
            padx=20,
            pady=5,
            command=self.start_game,
        )
        self.start_button.pack(side="left", padx=10)

        self.restart_button = tk.Button(
            self.button_frame,
            text="重新开始",
            font=self.button_font,
            fg="#fff",
            bg="#e94560",
            activebackground="#c73e54",
            activeforeground="#fff",
            relief="flat",
            padx=20,
            pady=5,
            command=self.restart_game,
            state="disabled",
        )
        self.restart_button.pack(side="left", padx=10)

        self.game_over_text = None
        self.score = 0
        self.snake = []
        self.food = None
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_running = False
        self.game_speed = 150

        self.window.bind("<KeyPress>", self.on_key_press)
        self.center_window()

    def center_window(self):
        self.window.update_idletasks()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - self.window.winfo_width()) // 2
        y = (screen_height - self.window.winfo_height()) // 2
        self.window.geometry(f"+{x}+{y}")

    def start_game(self):
        self.start_button.config(state="disabled")
        self.restart_button.config(state="normal")
        self.init_game()
        self.game_running = True
        self.game_loop()

    def restart_game(self):
        self.canvas.delete("all")
        self.game_over_text = None
        self.start_game()

    def init_game(self):
        self.score = 0
        self.score_label.config(text=f"分数: {self.score}")
        self.direction = "Right"
        self.next_direction = "Right"
        self.game_speed = 150

        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        self.snake = [(center_x, center_y), (center_x - 1, center_y), (center_x - 2, center_y)]
        self.place_food()

    def place_food(self):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break

    def on_key_press(self, event):
        key_map = {
            "Up": "Up",
            "Down": "Down",
            "Left": "Left",
            "Right": "Right",
            "w": "Up",
            "s": "Down",
            "a": "Left",
            "d": "Right",
        }
        new_direction = key_map.get(event.keysym)
        if new_direction:
            opposite = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
            if opposite.get(new_direction) != self.direction:
                self.next_direction = new_direction

    def game_loop(self):
        if not self.game_running:
            return

        self.direction = self.next_direction
        head_x, head_y = self.snake[0]

        direction_map = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}
        dx, dy = direction_map[self.direction]
        new_head = (head_x + dx, head_y + dy)

        if (
            new_head in self.snake
            or new_head[0] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] < 0
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:
            self.score += 10
            self.score_label.config(text=f"分数: {self.score}")
            self.place_food()
            if self.game_speed > 80:
                self.game_speed -= 2
        else:
            self.snake.pop()

        self.draw()
        self.window.after(self.game_speed, self.game_loop)

    def draw(self):
        self.canvas.delete("all")

        for x, y in self.snake:
            color = "#4ecca3" if (x, y) == self.snake[0] else "#45b393"
            self.canvas.create_rectangle(
                x * CELL_SIZE,
                y * CELL_SIZE,
                (x + 1) * CELL_SIZE,
                (y + 1) * CELL_SIZE,
                fill=color,
                outline="#1a1a2e",
                width=1,
            )

        food_x, food_y = self.food
        self.canvas.create_oval(
            food_x * CELL_SIZE + 2,
            food_y * CELL_SIZE + 2,
            (food_x + 1) * CELL_SIZE - 2,
            (food_y + 1) * CELL_SIZE - 2,
            fill="#e94560",
            outline="",
        )

    def game_over(self):
        self.game_running = False
        self.canvas.create_rectangle(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT, fill="#1a1a2e")
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 - 20,
            text="游戏结束",
            font=self.title_font,
            fill="#e94560",
            justify="center",
        )
        self.canvas.create_text(
            CANVAS_WIDTH // 2,
            CANVAS_HEIGHT // 2 + 20,
            text=f"最终分数: {self.score}",
            font=self.score_font,
            fill="#eee",
            justify="center",
        )

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = SnakeGame()
    game.run()
