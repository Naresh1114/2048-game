import tkinter as tk
import random

class Game2048:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("2048 Game")
        self.window.attributes("-fullscreen", True)  # Enable fullscreen mode
        self.grid = [[0] * 4 for _ in range(4)]
        self.cells = [[None] * 4 for _ in range(4)]
        self.score = 0

        self.initialize_ui()
        self.start_game()

    def initialize_ui(self):
        """Set up the game's user interface."""
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        cell_size = min(screen_width, screen_height) // 5  # Adjust cell size based on screen size

        self.frame = tk.Frame(self.window, bg="gray", bd=5)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the grid

        for i in range(4):
            for j in range(4):
                cell_frame = tk.Frame(self.frame, bg="lightgray", width=cell_size, height=cell_size)
                cell_frame.grid(row=i, column=j, padx=5, pady=5)
                label = tk.Label(
                    cell_frame, text="", bg="lightgray", font=("Helvetica", int(cell_size // 4), "bold")
                )
                label.grid()
                self.cells[i][j] = label

        self.score_label = tk.Label(
            self.window, text=f"Score: {self.score}", font=("Helvetica", int(cell_size // 5), "bold"), bg="gray"
        )
        self.score_label.pack(side="top", pady=20)

        self.exit_button = tk.Button(
            self.window, text="Exit", font=("Helvetica", int(cell_size // 6), "bold"), command=self.exit_game
        )
        self.exit_button.pack(side="bottom", pady=20)

        self.window.bind("<Key>", self.handle_keypress)

    def start_game(self):
        """Start a new game."""
        self.add_new_tile()
        self.add_new_tile()
        self.update_ui()

    def add_new_tile(self):
        """Add a new tile to a random empty cell."""
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        """Update the UI to reflect the current state of the grid."""
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                label = self.cells[i][j]
                if value == 0:
                    label.config(text="", bg="lightgray")
                else:
                    label.config(text=str(value), bg="orange", fg="white")
        self.score_label.config(text=f"Score: {self.score}")
        self.window.update_idletasks()

    def handle_keypress(self, event):
        """Handle keypresses to move tiles."""
        key = event.keysym
        old_grid = [row[:] for row in self.grid]

        if key == "Up":
            self.move_up()
        elif key == "Down":
            self.move_down()
        elif key == "Left":
            self.move_left()
        elif key == "Right":
            self.move_right()

        if self.grid != old_grid:
            self.add_new_tile()
            self.update_ui()

            if not self.can_move():
                self.show_game_over()

    def slide(self, row):
        """Slide all non-zero tiles in a row to the left."""
        new_row = [num for num in row if num != 0]
        new_row += [0] * (len(row) - len(new_row))
        return new_row

    def merge(self, row):
        """Merge adjacent tiles of the same value."""
        for i in range(len(row) - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def move_left(self):
        """Move the grid to the left."""
        for i in range(4):
            self.grid[i] = self.slide(self.grid[i])
            self.grid[i] = self.merge(self.grid[i])
            self.grid[i] = self.slide(self.grid[i])

    def move_right(self):
        """Move the grid to the right."""
        for i in range(4):
            self.grid[i] = self.slide(self.grid[i][::-1])
            self.grid[i] = self.merge(self.grid[i])
            self.grid[i] = self.slide(self.grid[i])
            self.grid[i] = self.grid[i][::-1]

    def move_up(self):
        """Move the grid up."""
        self.grid = list(map(list, zip(*self.grid)))
        self.move_left()
        self.grid = list(map(list, zip(*self.grid)))

    def move_down(self):
        """Move the grid down."""
        self.grid = list(map(list, zip(*self.grid)))
        self.move_right()
        self.grid = list(map(list, zip(*self.grid)))

    def can_move(self):
        """Check if any moves are possible."""
        for i in range(4):
            for j in range(4):
                if self.grid[i][j] == 0:
                    return True
                if j < 3 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
                if i < 3 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
        return False

    def show_game_over(self):
        """Show a game over message."""
        game_over_label = tk.Label(
            self.window, text="Game Over!", font=("Helvetica", 48, "bold"), fg="red", bg="gray"
        )
        game_over_label.pack(pady=50)

    def exit_game(self):
        """Exit the game."""
        self.window.destroy()

if __name__ == "__main__":
    game = Game2048()
    game.window.mainloop()
