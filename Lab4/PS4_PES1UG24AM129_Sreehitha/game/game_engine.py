
"""
GameEngine: owns the basket and all falling objects.

Task 1: Fix falling-object collision detection and list mutation.
Task 2: Keep the basket fully on screen with smooth movement.
Tasks 3 and 4 will be implemented separately.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 50
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        x = random.randint(20, WIDTH - 20)
        self.objects.append(FallingObject(x=x, y=-14, speed=3))

    def handle_input(self, keys_pressed):
        """Move smoothly while held, keeping the entire basket on screen."""
        if self.game_over:
            return

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Clamp the basket's center using half its width.
        half_width = self.basket.width / 2
        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x),
        )

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()

    def update(self):
        if self.game_over:
            return

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_object()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obj in self.objects:
            obj.update()

        # Task 1: check both horizontal and vertical overlap.
        basket_rect = self.basket.get_rect()

        # Check catches separately so iteration isn't disrupted by removals.
        caught_objects = [
            obj for obj in self.objects
            if is_caught(basket_rect, obj)
        ]

        for obj in caught_objects:
            self.score += 1
            self.objects.remove(obj)

        # Remove missed objects and update the miss counter.
        missed = [
            obj for obj in self.objects
            if obj.is_past_bottom(HEIGHT)
        ]

        if missed:
            self.objects = [
                obj for obj in self.objects
                if not obj.is_past_bottom(HEIGHT)
            ]

            self.misses += len(missed)

            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(
            surface, font, f"Score: {self.score}", (10, 10)
        )
        renderer.draw_text(
            surface,
            font,
            f"Misses: {self.misses}/{MAX_MISSES}",
            (10, 36),
        )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart.",
            )
