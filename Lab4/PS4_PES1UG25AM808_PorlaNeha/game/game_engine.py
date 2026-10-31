
import random
import pygame


class GameEngine:
    def __init__(self, width=560, height=390):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]

        # Adaptive AI
        self.player_history = []
        self.ai_randomness = 0.25

        # Scores and match settings
        self.player_score = 0
        self.cpu_score = 0
        self.target_score = 5
        self.game_over = False
        self.match_winner = None

        # Current round
        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.showing_result = False
        self.round_resolved_time = 0
        self.display_duration = 1200

        # Fonts
        self.font_title = pygame.font.SysFont(None, 36, bold=True)
        self.font_hud = pygame.font.SysFont(None, 25, bold=True)
        self.font_arena = pygame.font.SysFont(None, 27, bold=True)

        # Choice buttons
        button_width = 130
        button_height = 48
        gap = 20
        total_width = button_width * 3 + gap * 2
        start_x = (self.width - total_width) // 2
        button_y = self.height - button_height - 18

        self.buttons = [
            ChoiceButton(
                "ROCK",
                pygame.Rect(start_x, button_y, button_width, button_height),
                (165, 50, 50),
                (205, 75, 75),
            ),
            ChoiceButton(
                "PAPER",
                pygame.Rect(
                    start_x + button_width + gap,
                    button_y,
                    button_width,
                    button_height,
                ),
                (40, 100, 175),
                (60, 130, 205),
            ),
            ChoiceButton(
                "SCISSORS",
                pygame.Rect(
                    start_x + (button_width + gap) * 2,
                    button_y,
                    button_width,
                    button_height,
                ),
                (180, 140, 30),
                (210, 170, 45),
            ),
        ]

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"

        winning_moves = {
            "ROCK": "SCISSORS",
            "SCISSORS": "PAPER",
            "PAPER": "ROCK",
        }

        if winning_moves[player] == cpu:
            return "PLAYER"

        return "CPU"

    def predict_player_move(self):
        if not self.player_history:
            return random.choice(self.choices)

        move_counts = {
            move: self.player_history.count(move)
            for move in self.choices
        }

        highest_count = max(move_counts.values())

        most_common_moves = [
            move
            for move, count in move_counts.items()
            if count == highest_count
        ]

        return random.choice(most_common_moves)

    def play_round(self, choice):
        if self.game_over:
            return

        self.player_choice = choice

        # The CPU sometimes makes a random move to remain unpredictable.
        if (
            not self.player_history
            or random.random() < self.ai_randomness
        ):
            self.cpu_choice = random.choice(self.choices)
        else:
            predicted_move = self.predict_player_move()

            counter_moves = {
                "ROCK": "PAPER",
                "PAPER": "SCISSORS",
                "SCISSORS": "ROCK",
            }

            self.cpu_choice = counter_moves[predicted_move]

        # Record the player's move for future predictions.
        self.player_history.append(self.player_choice)

        outcome = self.determine_winner(
            self.player_choice,
            self.cpu_choice,
        )

        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = (
                f"You Win! {self.player_choice} beats {self.cpu_choice}."
            )
            self.result_color = (80, 230, 120)

        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = (
                f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            )
            self.result_color = (240, 80, 80)

        else:
            self.result_text = (
                f"It's a Draw! Both picked {self.player_choice}."
            )
            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

        # Check whether either side has reached five points.
        if self.player_score >= self.target_score:
            self.game_over = True
            self.match_winner = "PLAYER"
            self.result_text = "You won the match!"
            self.result_color = (80, 230, 120)

        elif self.cpu_score >= self.target_score:
            self.game_over = True
            self.match_winner = "CPU"
            self.result_text = "CPU won the match!"
            self.result_color = (240, 80, 80)

    def reset_game(self):
        self.player_score = 0
        self.cpu_score = 0
        self.game_over = False
        self.match_winner = None

        self.player_choice = None
        self.cpu_choice = None

        self.player_history = []

        self.showing_result = False
        self.round_resolved_time = 0

        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

    def handle_event(self, event):
        # Keyboard restart
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.reset_game()
                return

        # Mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            # Only the restart button is active after the match.
            if self.game_over:
                restart_rect = pygame.Rect(
                    self.width // 2 - 85,
                    300,
                    170,
                    38,
                )

                if restart_rect.collidepoint(event.pos):
                    self.reset_game()

                return

            # Normal game choices
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.play_round(btn.choice_name)
                    return

    def update(self):
        if self.showing_result and not self.game_over:
            current_time = pygame.time.get_ticks()

            if (
                current_time - self.round_resolved_time
                >= self.display_duration
            ):
                self.showing_result = False

    def draw_gesture(self, screen, choice, center, size=70):
        x, y = center

        if choice == "ROCK":
            color = (190, 145, 115)

            pygame.draw.rect(
                screen,
                color,
                (
                    x - size // 3,
                    y - size // 4,
                    2 * size // 3,
                    size // 2,
                ),
                border_radius=12,
            )

            pygame.draw.circle(
                screen,
                (225, 185, 150),
                (x - size // 8, y - size // 4),
                max(4, size // 7),
            )

            pygame.draw.circle(
                screen,
                (225, 185, 150),
                (x + size // 8, y - size // 4),
                max(4, size // 7),
            )

        elif choice == "PAPER":
            skin = (225, 185, 150)

            pygame.draw.rect(
                screen,
                skin,
                (
                    x - size // 3,
                    y - size // 5,
                    2 * size // 3,
                    size // 2,
                ),
                border_radius=8,
            )

            for offset in (-20, -10, 0, 10, 20):
                pygame.draw.rect(
                    screen,
                    skin,
                    (
                        x + offset * size / 70 - size // 18,
                        y - size // 2,
                        max(5, size // 9),
                        size // 2,
                    ),
                    border_radius=4,
                )

        elif choice == "SCISSORS":
            skin = (225, 185, 150)

            pygame.draw.rect(
                screen,
                skin,
                (
                    x - size // 4,
                    y,
                    size // 2,
                    size // 2,
                ),
                border_radius=10,
            )

            pygame.draw.line(
                screen,
                skin,
                (x - size // 10, y + size // 8),
                (x - size // 3, y - size // 2),
                max(6, size // 6),
            )

            pygame.draw.line(
                screen,
                skin,
                (x + size // 10, y + size // 8),
                (x + size // 3, y - size // 2),
                max(6, size // 6),
            )

    def render(self, screen):
        screen.fill((24, 28, 36))

        # Title
        title_surf = self.font_title.render(
            "Rock Paper Scissors",
            True,
            (245, 245, 245),
        )

        screen.blit(
            title_surf,
            (
                self.width // 2 - title_surf.get_width() // 2,
                12,
            ),
        )

        # Scores
        p_surf = self.font_hud.render(
            f"Player Score: {self.player_score}",
            True,
            (100, 180, 255),
        )

        c_surf = self.font_hud.render(
            f"CPU Score: {self.cpu_score}",
            True,
            (255, 120, 120),
        )

        screen.blit(p_surf, (25, 52))

        screen.blit(
            c_surf,
            (
                self.width - c_surf.get_width() - 25,
                52,
            ),
        )

        pygame.draw.line(
            screen,
            (45, 52, 66),
            (20, 82),
            (self.width - 20, 82),
            2,
        )

        # Selected moves
        p_str = self.player_choice if self.player_choice else "--"
        c_str = self.cpu_choice if self.cpu_choice else "--"

        arena_p = self.font_arena.render(
            f"Your Pick: {p_str}",
            True,
            (225, 225, 230),
        )

        arena_c = self.font_arena.render(
            f"CPU Pick: {c_str}",
            True,
            (225, 225, 230),
        )

        screen.blit(
            arena_p,
            (
                self.width // 2 - arena_p.get_width() // 2,
                105,
            ),
        )

        screen.blit(
            arena_c,
            (
                self.width // 2 - arena_c.get_width() // 2,
                140,
            ),
        )

        # Round result
        res_surf = self.font_arena.render(
            self.result_text,
            True,
            self.result_color,
        )

        screen.blit(
            res_surf,
            (
                self.width // 2 - res_surf.get_width() // 2,
                180,
            ),
        )

        if self.game_over:
            # Match-over screen
            banner_text = (
                "YOU WIN THE MATCH!"
                if self.match_winner == "PLAYER"
                else "CPU WINS THE MATCH!"
            )

            banner = self.font_arena.render(
                banner_text,
                True,
                (255, 215, 90),
            )

            screen.blit(
                banner,
                (
                    self.width // 2 - banner.get_width() // 2,
                    225,
                ),
            )

            # Draw the restart button above the bottom edge.
            restart_rect = pygame.Rect(
                self.width // 2 - 85,
                285,
                170,
                38,
            )

            pygame.draw.rect(
                screen,
                (45, 130, 85),
                restart_rect,
                border_radius=8,
            )

            pygame.draw.rect(
                screen,
                (230, 230, 235),
                restart_rect,
                width=2,
                border_radius=8,
            )

            restart_text = self.font_hud.render(
                "RESTART",
                True,
                (255, 255, 255),
            )

            screen.blit(
                restart_text,
                (
                    restart_rect.centerx - restart_text.get_width() // 2,
                    restart_rect.centery - restart_text.get_height() // 2,
                ),
            )

        else:
            # Animated gesture icons during the match
            if self.player_choice and self.cpu_choice:
                elapsed = pygame.time.get_ticks() - self.round_resolved_time
                icon_size = min(70, 45 + elapsed // 15)

                self.draw_gesture(
                    screen,
                    self.player_choice,
                    (self.width // 2 - 110, 270),
                    icon_size,
                )

                self.draw_gesture(
                    screen,
                    self.cpu_choice,
                    (self.width // 2 + 110, 270),
                    icon_size,
                )

            # Choice buttons are hidden when the match ends.
            for btn in self.buttons:
                btn.render(screen)


class ChoiceButton:
    def __init__(self, choice_name, rect, color, hover_color):
        self.choice_name = choice_name
        self.rect = rect
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont(None, 26)

    def contains(self, pos):
        return self.rect.collidepoint(pos)

    def render(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        bg_color = (
            self.hover_color
            if self.rect.collidepoint(mouse_pos)
            else self.color
        )

        pygame.draw.rect(
            surface,
            bg_color,
            self.rect,
            border_radius=8,
        )

        pygame.draw.rect(
            surface,
            (230, 230, 235),
            self.rect,
            width=2,
            border_radius=8,
        )

        text_surf = self.font.render(
            self.choice_name,
            True,
            (255, 255, 255),
        )

        surface.blit(
            text_surf,
            (
                self.rect.centerx - text_surf.get_width() // 2,
                self.rect.centery - text_surf.get_height() // 2,
            ),

        )
