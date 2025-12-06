import tkinter as tk
from tkinter import messagebox

import random
import time



def generate_maze(w, h):
    
    maze = [[1 for _ in range(w)] for _ in range(h)]
    stack = []

    start_x, start_y = 1, 1
    maze[start_y][start_x] = 0
    stack.append((start_x, start_y))

    directions = [(2, 0), (0, 2), (-2, 0), (0, -2)]

    while stack:
        x, y = stack[-1]

        neighbors = []
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 < nx < w - 1 and 0 < ny < h - 1 and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx, dy))

        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()

    return maze

def find_solution(maze, start, end):
    from collections import deque
    h, w = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start: None}

    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    while queue:
        x, y = queue.popleft()

        if (x, y) == end:
            path = []
            current = end
            while current is not None:
                path.append(current)
                current = visited[current]
            return path[::-1]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < w and 0 <= ny < h and maze[ny][nx] == 0 and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))

    return []



MAZE_WIDTH = 31
MAZE_HEIGHT = 21

maze = []
player_pos = [1, 1]
start_pos = (1, 1)
end_pos = (MAZE_WIDTH - 2, MAZE_HEIGHT - 2)
solution_path = []
show_solution = False
player_trail = []

# Timer variables
start_time = None



root = tk.Tk()
root.title("Maze Explorer")
root.configure(bg="#f5f5f7")
root.resizable(False, False)

BG_COLOR = "#f5f5f7"
WALL_COLOR = "#d4d4d8"
PATH_COLOR = "#ffffff"
PLAYER_COLOR = "#ecabe3"
START_COLOR = "#6ad8f0"
END_COLOR = "#96e7a2"
SOLUTION_COLOR = "#fde047"
TRAIL_COLOR = "#e9d5ff"
TEXT_COLOR = "#3f3f46"
BUTTON_BG = "#ffffff"
BUTTON_FG = "#3f3f46"

CELL_SIZE = 25

title_frame = tk.Frame(root, bg=BG_COLOR, pady=15)
title_frame.pack()

title_label = tk.Label(
    title_frame,
    text="🧩 Maze Explorer",
    font=("Arial", 24, "bold"),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
title_label.pack()

# TIMER LABEL (replaces steps)
step_label = tk.Label(
    title_frame,
    text="Time: 0.00s",
    font=("Arial", 14),
    bg=BG_COLOR,
    fg=TEXT_COLOR
)
step_label.pack(pady=(5, 0))

canvas_frame = tk.Frame(root, bg=BG_COLOR, padx=20, pady=10)
canvas_frame.pack()

canvas = tk.Canvas(
    canvas_frame,
    width=MAZE_WIDTH * CELL_SIZE,
    height=MAZE_HEIGHT * CELL_SIZE,
    bg=PATH_COLOR,
    highlightthickness=0,
    bd=0
)
canvas.pack()

button_frame = tk.Frame(root, bg=BG_COLOR, pady=15)
button_frame.pack()

def create_button(parent, text, command):
    btn = tk.Button(
        parent,
        text=text,
        command=command,
        font=("Arial", 11),
        bg=BUTTON_BG,
        fg=BUTTON_FG,
        activebackground="#e5e5e7",
        activeforeground=TEXT_COLOR,
        relief="flat",
        padx=20,
        pady=10,
        cursor="hand2",
        bd=0
    )
    return btn


def draw_maze():
    canvas.delete("all")

    for y in range(len(maze)):
        for x in range(len(maze[0])):
            px = x * CELL_SIZE
            py = y * CELL_SIZE

            if maze[y][x] == 1:
                canvas.create_rectangle(
                    px + 2, py + 2,
                    px + CELL_SIZE + 2, py + CELL_SIZE + 2,
                    fill="#c4c4c8", outline=""
                )
                canvas.create_rectangle(
                    px, py,
                    px + CELL_SIZE, py + CELL_SIZE,
                    fill=WALL_COLOR, outline=""
                )

    if show_solution and solution_path:
        for x, y in solution_path:
            px = x * CELL_SIZE + CELL_SIZE // 2
            py = y * CELL_SIZE + CELL_SIZE // 2
            canvas.create_oval(
                px - 4, py - 4, px + 4, py + 4,
                fill=SOLUTION_COLOR, outline=""
            )

    for x, y in player_trail:
        px = x * CELL_SIZE + CELL_SIZE // 2
        py = y * CELL_SIZE + CELL_SIZE // 2
        canvas.create_oval(
            px - 3, py - 3, px + 3, py + 3,
            fill=TRAIL_COLOR, outline=""
        )

    sx = start_pos[0] * CELL_SIZE
    sy = start_pos[1] * CELL_SIZE
    canvas.create_rectangle(
        sx + 3, sy + 3,
        sx + CELL_SIZE - 3, sy + CELL_SIZE - 3,
        fill=START_COLOR, outline=""
    )

    ex = end_pos[0] * CELL_SIZE
    ey = end_pos[1] * CELL_SIZE
    canvas.create_rectangle(
        ex + 3, ey + 3,
        ex + CELL_SIZE - 3, ey + CELL_SIZE - 3,
        fill=END_COLOR, outline=""
    )

    px = player_pos[0] * CELL_SIZE + CELL_SIZE // 2
    py = player_pos[1] * CELL_SIZE + CELL_SIZE // 2
    radius = CELL_SIZE // 3

    canvas.create_oval(
        px - radius + 2, py - radius + 2,
        px + radius + 2, py + radius + 2,
        fill="#c4c4c8", outline=""
    )
    canvas.create_oval(
        px - radius, py - radius,
        px + radius, py + radius,
        fill=PLAYER_COLOR, outline=""
    )



def new_maze():
    global maze, player_pos, solution_path, show_solution, player_trail, start_time
    maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
    player_pos = [start_pos[0], start_pos[1]]
    solution_path = find_solution(maze, start_pos, end_pos)
    show_solution = False
    player_trail = []
    start_time = time.time()
    step_label.config(text="Time: 0.00s")
    draw_maze()

def toggle_solution():
    global show_solution
    show_solution = not show_solution
    draw_maze()

def reset_player():
    global player_pos, player_trail, start_time
    player_pos = [start_pos[0], start_pos[1]]
    player_trail = []
    start_time = time.time()
    step_label.config(text="Time: 0.00s")
    draw_maze()

def move_player(dx, dy):
    global player_pos

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy

    if 0 <= new_x < MAZE_WIDTH and 0 <= new_y < MAZE_HEIGHT:
        if maze[new_y][new_x] == 0:
            if tuple(player_pos) not in player_trail:
                player_trail.append(tuple(player_pos))

            player_pos[0] = new_x
            player_pos[1] = new_y

            # Update timer
            if start_time:
                elapsed = time.time() - start_time
                step_label.config(text=f"Time: {elapsed:.2f}s")

            draw_maze()

            if player_pos[0] == end_pos[0] and player_pos[1] == end_pos[1]:
                elapsed = time.time() - start_time
                root.after(100, lambda: messagebox.showinfo(
                    "Maze Completed! 🎉",
                    f"You completed the maze in {elapsed:.2f} seconds!"
                ))

def on_key_press(event):
    if event.keysym == "Up":
        move_player(0, -1)
    elif event.keysym == "Down":
        move_player(0, 1)
    elif event.keysym == "Left":
        move_player(-1, 0)
    elif event.keysym == "Right":
        move_player(1, 0)



btn_new = create_button(button_frame, "🎲 New Maze", new_maze)
btn_new.grid(row=0, column=0, padx=5)

btn_solution = create_button(button_frame, "💡 Show Solution", toggle_solution)
btn_solution.grid(row=0, column=1, padx=5)

btn_reset = create_button(button_frame, "🔄 Reset Player", reset_player)
btn_reset.grid(row=0, column=2, padx=5)

root.bind("<KeyPress>", on_key_press)
root.focus_set()



new_maze()
root.mainloop()
