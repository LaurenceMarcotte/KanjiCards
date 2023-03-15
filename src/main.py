# -*- coding: utf-8 -*-
import pygame

from util_ui import Controller, SCREEN_HEIGHT, SCREEN_WIDTH


    

if __name__ == "__main__":

    # pygame.init()
    fps = 60
    fpsClock = pygame.time.Clock()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Kanji Cards")

    font = pygame.font.SysFont('Arial', 40)

    screenController = Controller(screen)

    while True:
        screen.fill((202, 228, 241))

        screenController.handle_events()

        screenController.draw()

        pygame.display.flip()
        fpsClock.tick(fps)
