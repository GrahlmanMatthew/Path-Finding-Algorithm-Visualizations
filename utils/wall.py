import pygame

class Wall(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], 16, 16)