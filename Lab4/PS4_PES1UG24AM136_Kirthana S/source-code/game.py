
from board import Board
import copy


class Game:
    def __init__(self):
        self.board = Board()
        self.best_score = 0
        self.history = []
        self.won = False

    def display(self):
        print("\n" + "+------+------+------+------+")
        for row in self.board.grid:
            print("|" + "|".join(f"{x:^6}" if x else f"{' ':^6}" for x in row) + "|")
            print("+------+------+------+------+")
        print("Score:", self.board.score, " Best:", self.best_score)


    def move(self, key):
        moves = {
            "a": self.board.move_left,
            "d": self.board.move_right,
            "w": self.board.move_up,
            "s": self.board.move_down,
        }

        if key not in moves:
            print("Invalid input. Use W/A/S/D.")
            return False

        old_grid = [row[:] for row in self.board.grid]
        old_score = self.board.score

        changed = moves[key]()

        if not changed:
            print("Move did not change the board.")
            return False

        self.history.append((old_grid, old_score))
        self.board.add_random_tile()
        self.best_score = max(self.best_score, self.board.score)

        if self.board.score > old_score:
            print(f"Successful move! You earned {self.board.score - old_score} points from merges.")
        else:
            print("Move successful.")

        return True


    def undo(self):
        if not self.history:
            print("Nothing to undo.")
            return False

        grid, score = self.history.pop()
        self.board.grid = grid
        self.board.score = score
        print("Previous move undone.")
        return True

    def run(self):
        print("2048 — W/A/S/D to move, U to undo, Q to quit.")

        while True:
            self.display()

            if any(value >= 2048 for row in self.board.grid for value in row):
                self.won = True
                print("You reached 2048!")
                return

            if not self.board.can_move():
                print("No legal moves remain.")
                return

            key = input("> ").strip().lower()

            if key == "q":
                return

            if key == "u":
                self.undo()
                continue

            if key not in "wasd":
                print("Use W/A/S/D.")
                continue

            if not self.move(key):
                print("Move did not change the board.")
