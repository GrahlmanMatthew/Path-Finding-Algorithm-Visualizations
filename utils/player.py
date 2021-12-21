import pygame
from utils.wall import Wall
from utils import level as LEVEL
from utils import colours as COLOURS

class Player(object):
    def __init__(self, x, y):
        self.start_x, self.start_y = x-2, y-2 # -2 here b4
        self.size = 20
        self.dist = 18
        self.rect = pygame.Rect(self.start_x, self.start_y, self.size, self.size)

    def drawPlayer(self, screen, colour=COLOURS.YELLOW):
        pygame.draw.rect(screen, colour, self.rect)

    def checkAdj(self, level, walls):
        left_tile = level[int(self.rect.y/18)+1][int((self.rect.x - self.dist)/18)+1]
        up_tile = level[int((self.rect.y-self.dist)/18)+1][int(self.rect.x/18)+1]
        down_tile = level[int((self.rect.y+self.dist)/18)+1][int(self.rect.x/18)+1]
        right_tile = level[int(self.rect.y/18)+1][int((self.rect.x + self.dist)/18)+1]
        return (left_tile, up_tile, down_tile, right_tile)

    def getDist(self):
        return self.dist

    def moveTopologicalPath(self, path, ind, player, level, walls):
        if not ind >= len(path)-1:
            diffx = (path[ind+1][0] - path[ind][0]) * self.dist
            diffy = (path[ind+1][1] - path[ind][1]) * self.dist
            marker = 'V'
            player.move(level, walls, marker, diffx, diffy)       

    def determineMove(self, player, level, walls):
        adj = player.checkAdj(level, walls)
        wall_counter = adj.count('W') + adj.count('X')
        marker = 'X' if wall_counter >= 3 else 'V'
        x_marker = 'X'
                            
        if adj[0] == ' ' or adj[0] == 'E':  player.move(level, walls, marker, -self.dist, 0)   
        elif adj[1] == ' ' or adj[1] == 'E':    player.move(level, walls, marker, 0, -self.dist)
        elif adj[2] == ' ' or adj[2] == 'E':    player.move(level, walls, marker, 0, self.dist)       
        elif adj[3] == ' ' or adj[3] == 'E':    player.move(level, walls, marker, self.dist, 0)
        elif adj[0] == 'V': player.move(level, walls, x_marker, -self.dist, 0)
        elif adj[1] == 'V': player.move(level, walls, x_marker, 0, -self.dist)
        elif adj[2] == 'V': player.move(level, walls, x_marker, 0, self.dist)
        elif adj[3] == 'V': player.move(level, walls, x_marker, self.dist, 0)

    def generateDirectedAcyclicGraph(self, path_tree, player, level, walls, curr_xy):
        adj = player.checkAdj(level, walls)
        wall_counter = adj.count('W') + adj.count('X')
        marker = 'X' if wall_counter >= 3 else 'V'
        x_marker = 'X'
        children = path_tree.get(curr_xy)
        
        
        if adj[0] == ' ' or adj[0] == 'E':
            player.move(level, walls, marker, -self.dist, 0)   
            children['left'] = (curr_xy[0] - 1, curr_xy[1])     
        elif adj[1] == ' ' or adj[1] == 'E':
            player.move(level, walls, marker, 0, -self.dist)
            children['up'] = (curr_xy[0], curr_xy[1]-1)            
        elif adj[2] == ' ' or adj[2] == 'E':
            player.move(level, walls, marker, 0, self.dist)       
            children['down'] = (curr_xy[0], curr_xy[1]+1)
        elif adj[3] == ' ' or adj[3] == 'E':
            player.move(level, walls, marker, self.dist, 0)
            children['right'] = (curr_xy[0]+1, curr_xy[1])
        elif adj[0] == 'V': player.move(level, walls, x_marker, -self.dist, 0)
        elif adj[1] == 'V': player.move(level, walls, x_marker, 0, -self.dist)
        elif adj[2] == 'V': player.move(level, walls, x_marker, 0, self.dist)
        elif adj[3] == 'V': player.move(level, walls, x_marker, self.dist, 0)
        path_tree[curr_xy[0], curr_xy[1]] = children
        
            
    def move(self, lvl, wlls, marker, dx, dy):
        self.move_single_axis(lvl, wlls, marker, dx, dy)
            
    def move_single_axis(self, lvl, wlls, marker, dx, dy): # moves rect obj
        lvl[int((self.rect.y)/self.dist)+1][int((self.rect.x)/self.dist)+1] = marker
        
        self.rect.x += dx     
        self.rect.y += dy
        
        lvl[int((self.rect.y)/self.dist)+1][int((self.rect.x)/self.dist)+1] = 'P'
        self.collision(wlls, dx, dy)
        
    def collision(self, wlls, dx, dy):
        for wall in wlls:
            if self.rect.colliderect(wall.rect):
                if dx > 0:  self.rect.right = wall.rect.left
                if dx < 0:  self.rect.left = wall.rect.right
                if dy > 0:  self.rect.bottom = wall.rect.top
                if dy < 0:  self.rect.top = wall.rect.bottom