import os, sys, time, copy, random, pygame
from utils.wall import Wall
from utils import level as LEVEL
from utils import colours as COLOURS
from utils.pathfinder import createDAG
from utils.levelParser import LevelParser

def draw(screen, level_parser, player, player2):
    screen.fill((0, 0, 0))
    level_parser.drawLevel(screen)
    player2.drawPlayer(screen, colour=COLOURS.GREEN)
    player.drawPlayer(screen) 
    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("DAG Path Finder")
    screen = pygame.display.set_mode((450, 450))    # prev 360, 270
    clock = pygame.time.Clock()

    print('\nExhaustive Search vs. Topological Order in Directed Acyclic Graphs (DAGs)')
    print('---------------------------------------------------------------------------')

    levels = [
        LEVEL.LEVEL1.splitlines()[1:],
        LEVEL.LEVEL2.splitlines()[1:],
        LEVEL.LEVEL3.splitlines()[1:],
        LEVEL.LEVEL4.splitlines()[1:],
        LEVEL.LEVEL5.splitlines()[1:] 
    ]
    
    exhaust_times = []
    top_times = []

    for level in levels:
        level_parser, graph_parser, top_parser = LevelParser(level), LevelParser(level), LevelParser(level)
        level_array = level_parser.getLevelArray(level)
        
        player, graph_player, top_player = level_parser.getPlayer(), graph_parser.getPlayer(), top_parser.getPlayer()
        walls, start, finish = level_parser.getWalls(), level_parser.getStart(), level_parser.getFinish()

        top_index = 0
        train_array = copy.deepcopy(level_array)
        path = createDAG(train_array, graph_player, walls, start, finish)
        exhaust_array, top_game_array = copy.deepcopy(level_array), copy.deepcopy(level_array)
        
        start_time = time.time()
        exh, top = True, True
        while exh or top:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
            
            player.determineMove(player, exhaust_array, walls)  # EXHAUSTIVE SEARCH

            top_player.moveTopologicalPath(path, top_index, top_player, top_game_array, walls) # TOPOLOGICAL ORDER
            top_index += 1
        
            if top_player.rect.colliderect(finish) and top:
                exec_time = float(time.time() - start_time)
                top_times.append(exec_time)               
                print('Level %s - Topological Order Search Time: %s seconds' % (levels.index(level) + 1, exec_time))
                draw(screen, level_parser, player, top_player)
                top = False
        
            if player.rect.colliderect(finish):
                exec_time = time.time() - start_time
                exhaust_times.append(exec_time)
                print('Level %s - Exhaustive Search Time: %s seconds' % (levels.index(level) + 1, exec_time))
                draw(screen, level_parser, player, top_player)
                exh = False
                
            if not exh and not top:
                print('')
                break

            draw(screen, level_parser, player, top_player)
            clock.tick(45)
            time.sleep(0.0001)

    pygame.quit()
    
    avg_exh, avg_top = 0, 0
    for val in top_times:
        avg_top += val
    avg_top /= len(top_times)
    print("Avg. Topological Order Search Time: %s" % avg_top)
    
    for val in exhaust_times:
        avg_exh += val
    avg_exh /= len(exhaust_times)
    print("Avg. Exhaustive Search Time: %s" % avg_exh)
    
    ratio = avg_exh / avg_top
    print("On averaage, TO outperforms EXH by: %s times" % ratio)
    
main()