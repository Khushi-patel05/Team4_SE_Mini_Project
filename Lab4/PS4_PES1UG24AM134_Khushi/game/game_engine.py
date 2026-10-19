
import pygame
import time
import json
import os
from collections import deque
from game.maze import generate_maze, CELL
from game.player import Player

FPS = 60
BG = (240, 235, 220)
WALL_COLOR = (40, 40, 60)
EXIT_COLOR = (80, 200, 80)
PATH_COLOR = (255, 215, 0)
COLS, ROWS = 15, 13

WIDTH = COLS * CELL
HEIGHT = ROWS * CELL + 60
LEADERBOARD_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "leaderboard.json",
)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.big_font = pygame.font.SysFont("monospace", 36, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 17)
        self.reset()

    def load_leaderboard(self):
        """Load saved completion times from JSON."""
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                valid_times = [
                    float(entry)
                    for entry in data
                    if isinstance(entry, (int, float))
                    and not isinstance(entry, bool)
                    and entry >= 0
                ]
                return sorted(valid_times)[:5]
        except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
            pass
        return []

    def save_completion_time(self):
        """Save the latest completion time and retain the five fastest times."""
        leaderboard = self.load_leaderboard()
        leaderboard.append(round(self.elapsed, 2))
        leaderboard = sorted(leaderboard)[:5]

        try:
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
                json.dump(leaderboard, file, indent=4)
        except OSError as error:
            print(f"Could not save leaderboard: {error}")

        self.leaderboard = leaderboard

    def reset(self):
        self.walls = generate_maze(COLS, ROWS)
        self.player = Player(0, 0)
        self.exit_rect = pygame.Rect(
            (COLS - 1) * CELL + 5,
            (ROWS - 1) * CELL + 5,
            CELL - 10,
            CELL - 10,
        )
        self.start_time = time.time()
        self.elapsed = 0
        self.won = False
        self.completion_recorded = False
        self.show_path = False
        self.solution_path = self.find_shortest_path()
        self.leaderboard = self.load_leaderboard()

    def find_shortest_path(self):
        """Find the shortest path from start to exit using BFS."""
        start = (0, 0)
        target = (ROWS - 1, COLS - 1)
        queue = deque([start])
        parents = {start: None}

        directions = [
            (-1, 0, 0, 1),  # North
            (1, 0, 1, 0),   # South
            (0, 1, 2, 3),   # East
            (0, -1, 3, 2),  # West
        ]

        while queue:
            r, c = queue.popleft()

            if (r, c) == target:
                break

            for dr, dc, wall_dir, opposite_dir in directions:
                nr, nc = r + dr, c + dc

                if not (0 <= nr < ROWS and 0 <= nc < COLS):
                    continue
                if self.walls[r][c][wall_dir]:
                    continue

                neighbor = (nr, nc)
                if neighbor in parents:
                    continue

                parents[neighbor] = (r, c)
                queue.append(neighbor)

        if target not in parents:
            return []

        path = []
        current = target
        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        return path

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_h:
                    self.show_path = not self.show_path

        return True

    def update(self):
        if self.won:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, ROWS, COLS)
        self.elapsed = time.time() - self.start_time

        if self.player.rect.colliderect(self.exit_rect):
            self.elapsed = time.time() - self.start_time
            self.won = True

            if not self.completion_recorded:
                self.save_completion_time()
                self.completion_recorded = True

    def draw_maze(self):
        wall_w = 3

        for r in range(ROWS):
            for c in range(COLS):
                x, y = c * CELL, r * CELL
                w = self.walls[r][c]

                if w[0]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y), (x + CELL, y), wall_w
                    )
                if w[1]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y + CELL), (x + CELL, y + CELL), wall_w
                    )
                if w[2]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x + CELL, y), (x + CELL, y + CELL), wall_w
                    )
                if w[3]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y), (x, y + CELL), wall_w
                    )

    def draw_solution_path(self):
        """Draw colored squares along the BFS solution path."""
        if not self.show_path:
            return

        player_cell = (
            self.player.rect.centery // CELL,
            self.player.rect.centerx // CELL,
        )

        for r, c in self.solution_path:
            if (r, c) == player_cell:
                continue
            if (r, c) == (ROWS - 1, COLS - 1):
                continue

            rect = pygame.Rect(
                c * CELL + 10,
                r * CELL + 10,
                CELL - 20,
                CELL - 20,
            )
            pygame.draw.rect(
                self.screen, PATH_COLOR, rect, border_radius=5
            )

    def draw_fog_of_war(self):
        """Darken the maze beyond three cells from the player."""
        fog = pygame.Surface(
            (WIDTH, ROWS * CELL), pygame.SRCALPHA
        )
        fog.fill((0, 0, 0, 235))

        pygame.draw.circle(
            fog,
            (0, 0, 0, 0),
            self.player.rect.center,
            3 * CELL,
        )

        self.screen.blit(fog, (0, 0))

    def draw(self):
        self.screen.fill(BG)
        self.draw_maze()
        self.draw_solution_path()
        self.draw_fog_of_war()

        pygame.draw.rect(
            self.screen, EXIT_COLOR, self.exit_rect, border_radius=4
        )
        ex_label = self.font.render("EXIT", True, (20, 80, 20))
        self.screen.blit(
            ex_label,
            (self.exit_rect.x + 2, self.exit_rect.y + 4),
        )
        self.player.draw(self.screen)

        hud = pygame.Rect(0, ROWS * CELL, WIDTH, 60)
        pygame.draw.rect(self.screen, (30, 30, 50), hud)

        time_surf = self.font.render(
            f"Time: {self.elapsed:.1f}s   H = Hint   R = New Maze",
            True,
            (200, 200, 200),
        )
        self.screen.blit(time_surf, (10, ROWS * CELL + 18))

        if self.won:
            overlay = pygame.Surface(
                (WIDTH, ROWS * CELL), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))

            msg = self.big_font.render(
                f"Solved in {self.elapsed:.1f}s!",
                True,
                (80, 240, 80),
            )
            self.screen.blit(
                msg,
                (WIDTH // 2 - msg.get_width() // 2, 12),
            )

            title = self.font.render(
                "TOP 5 TIMES", True, (255, 215, 0)
            )
            self.screen.blit(
                title,
                (WIDTH // 2 - title.get_width() // 2, 58),
            )

            if self.leaderboard:
                for index, completion_time in enumerate(self.leaderboard):
                    line = self.small_font.render(
                        f"{index + 1}. {completion_time:.2f} seconds",
                        True,
                        (255, 255, 255),
                    )
                    self.screen.blit(
                        line,
                        (WIDTH // 2 - line.get_width() // 2, 88 + index * 25),
                    )
            else:
                line = self.small_font.render(
                    "No completion times yet",
                    True,
                    (255, 255, 255),
                )
                self.screen.blit(
                    line,
                    (WIDTH // 2 - line.get_width() // 2, 95),
                )

            sub = self.small_font.render(
                "Press R for a new maze",
                True,
                (200, 200, 200),
            )
            self.screen.blit(
                sub,
                (WIDTH // 2 - sub.get_width() // 2, ROWS * CELL - 35),
            )

        pygame.display.flip()

    def run(self):
        running = True

        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
