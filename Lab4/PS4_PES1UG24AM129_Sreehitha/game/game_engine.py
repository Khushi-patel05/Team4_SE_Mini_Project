
"""
GameEngine: owns the basket and all falling objects.

Task 1: Fix falling-object collision detection and list mutation.
Task 2: Keep the basket fully on screen with smooth movement.
Task 3: Vary object spawning positions and intervals, avoid repeated
        positions, keep spawns within the playable area, and cap the
        number of objects on screen.
Task 4: Add a temporary speed boost with a visible indicator.
"""

import random
import pygame

from game.basket import Basket
from game.falling_object import FallingObject
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT

MIN_SPAWN_INTERVAL_FRAMES = 30
MAX_SPAWN_INTERVAL_FRAMES = 65
MAX_OBJECTS_ON_SCREEN = 6
OBJECT_RADIUS = 14
OBJECT_SPAWN_MARGIN = OBJECT_RADIUS
MAX_SPAWN_ATTEMPTS = 10
MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.frames_until_spawn = 0
        self.last_spawn_x = None
        self.score = 0
        self.misses = 0
        self.game_over = False

    def _spawn_object(self):
        """Spawn an object at a varied, valid horizontal position."""
        if len(self.objects) >= MAX_OBJECTS_ON_SCREEN:
            return

        min_x = OBJECT_SPAWN_MARGIN
        max_x = WIDTH - OBJECT_SPAWN_MARGIN

        x = None

        # Avoid repeating the previous horizontal spawn position.
        for _ in range(MAX_SPAWN_ATTEMPTS):
            candidate_x = random.randint(min_x, max_x)

            if candidate_x != self.last_spawn_x:
                x = candidate_x
                break

        # Fallback if random attempts repeatedly select the same position.
        if x is None:
            if self.last_spawn_x is not None:
                x = min_x if self.last_spawn_x != min_x else max_x
            else:
                x = random.randint(min_x, max_x)

        self.last_spawn_x = x

        self.objects.append(
            FallingObject(
                x=x,
                y=-OBJECT_RADIUS,
                radius=OBJECT_RADIUS,
                speed=3,
            )
        )

    def handle_input(self, keys_pressed):
        """Move smoothly while held, keeping the basket on screen."""
        if self.game_over:
            return

        if keys_pressed[pygame.K_LEFT]:
            self.basket.x -= self.basket.speed

        if keys_pressed[pygame.K_RIGHT]:
            self.basket.x += self.basket.speed

        # Keep the entire basket within the screen boundaries.
        half_width = self.basket.width / 2
        self.basket.x = max(
            half_width,
            min(WIDTH - half_width, self.basket.x),
        )

    def handle_keydown(self, key):
        """Handle restart and speed-boost keyboard controls."""
        if self.game_over and key == pygame.K_r:
            self.__init__()
            return

        if not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        # Task 4: update the boost timer and restore normal speed on expiry.
        self.basket.update()

        # Task 3: spawn at varied intervals, subject to the object cap.
        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            if len(self.objects) < MAX_OBJECTS_ON_SCREEN:
                self._spawn_object()

            self.frames_until_spawn = random.randint(
                MIN_SPAWN_INTERVAL_FRAMES,
                MAX_SPAWN_INTERVAL_FRAMES,
            )

        for obj in self.objects:
            obj.update()

        # Task 1: check horizontal and vertical collision.
        basket_rect = self.basket.get_rect()

        # Collect caught objects separately to avoid mutating the list
        # while iterating over it.
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

        # Task 4: display the boost status and remaining duration.
        if self.basket.is_boosted():
            seconds_left = self.basket.boosted_frames / 60
            boost_text = f"SPEED BOOST! {seconds_left:.1f}s"
            renderer.draw_text(
                surface, font, boost_text, (10, 62)
            )
        else:
            renderer.draw_text(
                surface, font, "Press SPACE for speed boost",
                (10, 62),
            )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"Game Over! Final score: {self.score}. Press R to restart.",
            )
