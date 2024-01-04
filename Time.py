
import pygame
class Time:

    clock = pygame.time.Clock()
    deltaTime = 0

    @staticmethod
    def tick(frameRateCap):
        Time.deltaTime = Time.clock.tick(frameRateCap) / 1000.0  # Convert milliseconds to seconds