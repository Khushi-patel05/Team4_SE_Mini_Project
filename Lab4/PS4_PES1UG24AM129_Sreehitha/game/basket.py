"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.normal_speed = speed
        self.boost_speed = speed * 2
        self.speed = self.normal_speed

        self.boost_duration = 180  # 3 seconds at 60 FPS
        self.boosted_frames = 0

    def activate_boost(self):
        """Activate or refresh the temporary speed boost."""
        self.boosted_frames = self.boost_duration
        self.speed = self.boost_speed

    def update(self):
        """Count down the boost and restore normal speed when it expires."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1

            if self.boosted_frames == 0:
                self.speed = self.normal_speed

    def is_boosted(self):
        """Return whether the speed boost is currently active."""
        return self.boosted_frames > 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )