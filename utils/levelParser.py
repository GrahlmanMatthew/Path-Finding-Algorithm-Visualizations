import pygame
from utils.wall import Wall
from utils import colours as COLOURS
from utils.player import Player

class LevelParser:
    def __init__(self, level):
        self.walls = []
        self.parseLevel(level)
        
    def parseLevel(self, level):
        x,y = 1, 1
        for row in level:
            for col in row:
                if col == "W": self.walls.append(Wall((x, y)))
                if col == "E": self.finish = pygame.Rect(x, y, 15, 15)
                if col == "P":
                    self.start = (x,y)
                    self.player = Player(x, y)
                x += 18
            y += 18
            x = 1
         
    def getLevelArray(self, level):
        level_array = []
        for row in level:
            row_array = []
            for col in row:
                row_array.append(col)
            level_array.append(row_array)
        return level_array
            
    def getWalls(self):
        return self.walls
    
    def getPlayer(self):
        return self.player
            
    def getStart(self):
        return self.start
            
    def getFinish(self):
        return self.finish
    
    def drawLevel(self, screen):
        for wall in self.walls:
            pygame.draw.rect(screen, COLOURS.PURPLE, wall.rect)
        pygame.draw.rect(screen, COLOURS.RED, self.finish)
