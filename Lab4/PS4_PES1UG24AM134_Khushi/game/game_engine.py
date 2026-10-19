
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

DIFFICULTIES = {
    "Easy": (10, 8),
    "Medium": (15, 13),
    "Hard": (20, 18),
}

LEADERBOARD_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "leaderboard.json",
)


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 500))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 22)
        self.big_font = pygame.font.SysFont("monospace", 32, bold=True)
        self.small_font = pygame.font.SysFont("monospace", 17)

        self.menu = True
        self.difficulty_names = list(DIFFICULTIES.keys())
        self.selected_index = 1
        self.cols = 15
        self.rows = 13
        self.leaderboard = self.load_leaderboard()

    def load_leaderboard(self):
        """Load and return the five fastest saved completion times."""
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            if isinstance(data, list):
                valid_times = [
                    float(value)
                    for value in data
                    if isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and value >= 0
                ]
                return sorted(valid_times)[:5]

        except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
            pass

        return []

    def save_completion_time(self):
        """Save the five fastest completion times."""
        leaderboard = self.load_leaderboard()
        leaderboard.append(round(self.elapsed, 2))
        self.leaderboard = sorted(leaderboard)[:5]

        try:
            with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
                json.dump(self.leaderboard, file, indent=4)
        except OSError as error:
            print(f"Could not save leaderboard: {error}")

    def start_game(self):
        """Start a maze using the currently selected difficulty."""
        name = self.difficulty_names[self.selected_index]
        self.cols, self.rows = DIFFICULTIES[name]

        width = self.cols * CELL
        height = self.rows * CELL + 60
        self.screen = pygame.display.set_mode((width, height))

        self.reset()
        self.menu = False

    def reset(self):
        """Generate a new maze at the current difficulty."""
        self.walls = generate_maze(self.cols, self.rows)
        self.player = Player(0, 0)

        self.exit_rect = pygame.Rect(
            (self.cols - 1) * CELL + 5,
            (self.rows - 1) * CELL + 5,
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
        """Find the shortest route from start to exit using BFS."""
        start = (0, 0)
        target = (self.rows - 1, self.cols - 1)
        queue = deque([start])
        parents = {start: None}

        directions = [
            (-1, 0, 0, 1),
            (1, 0, 1, 0),
            (0, 1, 2, 3),
            (0, -1, 3, 2),
        ]

        while queue:
            r, c = queue.popleft()

            if (r, c) == target:
                break

            for dr, dc, wall_dir, opposite_dir in directions:
                nr, nc = r + dr, c + dc

                if not (0 <= nr < self.rows and 0 <= nc < self.cols):
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

            if event.type != pygame.KEYDOWN:
                continue

            if self.menu:
                if event.key in (pygame.K_UP, pygame.K_LEFT):
                    self.selected_index = (
                        self.selected_index - 1
                    ) % len(self.difficulty_names)

                elif event.key in (pygame.K_DOWN, pygame.K_RIGHT):
                    self.selected_index = (
                        self.selected_index + 1
                    ) % len(self.difficulty_names)

                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    self.start_game()

            else:
                if event.key == pygame.K_r:
                    self.reset()

                elif event.key == pygame.K_h:
                    self.show_path = not self.show_path

                elif event.key == pygame.K_ESCAPE:
                    self.menu = True
                    self.screen = pygame.display.set_mode((600, 500))

        return True

    def update(self):
        if self.menu or self.won:
            return

        keys = pygame.key.get_pressed()
        self.player.move(keys, self.walls, self.rows, self.cols)
        self.elapsed = time.time() - self.start_time

        if self.player.rect.colliderect(self.exit_rect):
            self.elapsed = time.time() - self.start_time
            self.won = True

            if not self.completion_recorded:
                self.save_completion_time()
                self.completion_recorded = True

    def draw_menu(self):
        self.screen.fill((25, 25, 45))

        title = self.big_font.render(
            "MAZE RUNNER", True, (255, 215, 0)
        )
        self.screen.blit(
            title,
            (300 - title.get_width() // 2, 75),
        )

        prompt = self.font.render(
            "Choose Difficulty", True, (240, 240, 240)
        )
        self.screen.blit(
            prompt,
            (300 - prompt.get_width() // 2, 155),
        )

        for index, name in enumerate(self.difficulty_names):
            cols, rows = DIFFICULTIES[name]
            selected = index == self.selected_index

            color = (255, 215, 0) if selected else (210, 210, 220)
            prefix = "> " if selected else "  "

            label = self.font.render(
                f"{prefix}{name}: {cols} x {rows}",
                True,
                color,
            )
            self.screen.blit(
                label,
                (300 - label.get_width() // 2, 215 + index * 45),
            )

        hint = self.small_font.render(
            "UP/DOWN to choose - ENTER to start",
            True,
            (180, 180, 190),
        )
        self.screen.blit(
            hint,
            (300 - hint.get_width() // 2, 390),
        )

        pygame.display.flip()

    def draw_maze(self):
        wall_w = 3

        for r in range(self.rows):
            for c in range(self.cols):
                x, y = c * CELL, r * CELL
                walls = self.walls[r][c]

                if walls[0]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y), (x + CELL, y), wall_w
                    )
                if walls[1]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y + CELL), (x + CELL, y + CELL), wall_w
                    )
                if walls[2]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x + CELL, y), (x + CELL, y + CELL), wall_w
                    )
                if walls[3]:
                    pygame.draw.line(
                        self.screen, WALL_COLOR,
                        (x, y), (x, y + CELL), wall_w
                    )

    def draw_solution_path(self):
        if not self.show_path:
            return

        player_cell = (
            self.player.rect.centery // CELL,
            self.player.rect.centerx // CELL,
        )

        for r, c in self.solution_path:
            if (r, c) == player_cell:
                continue

            if (r, c) == (self.rows - 1, self.cols - 1):
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
        width = self.cols * CELL
        height = self.rows * CELL

        fog = pygame.Surface((width, height), pygame.SRCALPHA)
        fog.fill((0, 0, 0, 235))

        pygame.draw.circle(
            fog,
            (0, 0, 0, 0),
            self.player.rect.center,
            3 * CELL,
        )

        self.screen.blit(fog, (0, 0))

    def draw(self):
        if self.menu:
            self.draw_menu()
            return

        width = self.cols * CELL
        maze_height = self.rows * CELL

        self.screen.fill(BG)
        self.draw_maze()
        self.draw_solution_path()
        self.draw_fog_of_war()

        pygame.draw.rect(
            self.screen, EXIT_COLOR, self.exit_rect, border_radius=4
        )
        exit_label = self.small_font.render(
            "EXIT", True, (20, 80, 20)
        )
        self.screen.blit(
            exit_label,
            (self.exit_rect.x + 2, self.exit_rect.y + 4),
        )

        self.player.draw(self.screen)

        hud = pygame.Rect(0, maze_height, width, 60)
        pygame.draw.rect(self.screen, (30, 30, 50), hud)

        time_text = self.font.render(
            f"Time: {self.elapsed:.1f}s  H=Hint  R=New Maze  ESC=Menu",
            True,
            (200, 200, 200),
        )
        self.screen.blit(time_text, (10, maze_height + 18))

        if self.won:
            overlay = pygame.Surface(
                (width, maze_height), pygame.SRCALPHA
            )
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))

            message = self.big_font.render(
                f"Solved in {self.elapsed:.1f}s!",
                True,
                (80, 240, 80),
            )
            self.screen.blit(
                message,
                (width // 2 - message.get_width() // 2, 12),
            )

            title = self.font.render(
                "TOP 5 TIMES", True, (255, 215, 0)
            )
            self.screen.blit(
                title,
                (width // 2 - title.get_width() // 2, 58),
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
                        (width // 2 - line.get_width() // 2, 88 + index * 25),
                    )
            else:
                line = self.small_font.render(
                    "No completion times yet",
                    True,
                    (255, 255, 255),
                )
                self.screen.blit(
                    line,
                    (width // 2 - line.get_width() // 2, 95),
                )

            subtitle = self.small_font.render(
                "Press R for a new maze",
                True,
                (200, 200, 200),
            )
            self.screen.blit(
                subtitle,
                (
                    width // 2 - subtitle.get_width() // 2,
                    maze_height - 35,
                ),
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
