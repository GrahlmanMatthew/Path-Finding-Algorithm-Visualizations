import os, sys, time, copy, random, pygame
from utils.wall import Wall
from utils import level as LEVEL
from utils import colours as COLOURS
from utils.pathfinder import createTopoDAG, createAStarGraph
from utils.levelParser import LevelParser

def draw(screen, level_parser, player, player2, player3, level_num):
    screen.fill((0, 0, 0))
    level_parser.drawLevel(screen, level_num)
    player3.drawPlayer(screen, colour=COLOURS.BLUE)
    player2.drawPlayer(screen, colour=COLOURS.GREEN)
    player.drawPlayer(screen) 
    pygame.display.flip()

def main():
    pygame.init()
    pygame.display.set_caption("Path Finder")
    screen = pygame.display.set_mode((450, 450))    # prev 360, 270
    clock = pygame.time.Clock()

    print('\nA* (BLUE) vs. Exhaustive Search (GREEN) vs. Topological Order (YELLOW) in Directed Graphs')
    print('---------------------------------------------------------------------------')

    levels = [
        LEVEL.LEVEL1.splitlines()[1:],
        LEVEL.LEVEL2.splitlines()[1:],
        LEVEL.LEVEL3.splitlines()[1:],
        LEVEL.LEVEL4.splitlines()[1:],
        LEVEL.LEVEL5.splitlines()[1:] 
    ]
    
    exhaust_times, top_times, astar_times = [], [], []
    for level in levels:
        level_num = levels.index(level) + 1
        level_parser, graph_parser, top_parser, astar_parser = LevelParser(level), LevelParser(level), LevelParser(level), LevelParser(level)
        level_array = level_parser.getLevelArray(level)
        
        player, graph_player, top_player, astar_player = level_parser.getPlayer(), graph_parser.getPlayer(), top_parser.getPlayer(), astar_parser.getPlayer()
        walls, start, finish = level_parser.getWalls(), level_parser.getStart(), level_parser.getFinish()

        train_array = copy.deepcopy(level_array)
        path = createTopoDAG(train_array, graph_player, walls, start, finish)   # TOP PATH
        
        allpaths = createAStarGraph(train_array, graph_player, walls, start, finish)
        astar_path = []
        if len(allpaths) > 0:
            astar_path = allpaths[0]
            
        for p in allpaths:
            if len(p) < len(astar_path):
                astar_path = p
        
        exhaust_array, top_game_array, astar_game_array = copy.deepcopy(level_array), copy.deepcopy(level_array), copy.deepcopy(level_array)
        
        animate_index = 0
        start_time = time.time()
        exh, top, astar = True, True, True
        while exh or top or astar:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                    running = False
            
            player.determineMove(player, exhaust_array, walls)  # EXHAUSTIVE SEARCH
            top_player.moveTopologicalPath(path, animate_index, top_player, top_game_array, walls) # TOPOLOGICAL SEARCH
            astar_player.moveTopologicalPath(astar_path, animate_index, astar_player, astar_game_array, walls)  # A* (SHORTEST PATH)
            animate_index += 1
        
            if astar_player.rect.colliderect(finish) and astar:
                exec_time = time.time() - start_time
                astar_times.append(exec_time)
                print('Level %s - A* (BLUE) Time: %s seconds' % (level_num, exec_time))
                draw(screen, level_parser, player, top_player, astar_player, level_num)
                astar = False
        
            if top_player.rect.colliderect(finish) and top:
                exec_time = float(time.time() - start_time)
                top_times.append(exec_time)               
                print('Level %s - Topological Order (GREEN) Search Time: %s seconds' % (level_num, exec_time))
                draw(screen, level_parser, player, top_player, astar_player, level_num)
                top = False
        
            if player.rect.colliderect(finish):
                exec_time = time.time() - start_time
                exhaust_times.append(exec_time)
                print('Level %s - Exhaustive Search (YELLOW) Time: %s seconds' % (level_num, exec_time))
                draw(screen, level_parser, player, top_player, astar_player, level_num)
                exh = False
                
            if not exh and not top and not astar:
                print('')
                break

            draw(screen, level_parser, player, top_player, astar_player, level_num)
            clock.tick(45)
            time.sleep(0.1)

    pygame.quit()
    
    avg_exh, avg_top, avg_astar = 0, 0, 0
    
    for val in astar_times:
        avg_astar += val
    avg_astar /= len(astar_times)
    print("Avg. A* Search Time: %s" % avg_astar)
    
    for val in top_times:
        avg_top += val
    avg_top /= len(top_times)
    print("Avg. Topological Order Search Time: %s" % avg_top)
    
    for val in exhaust_times:
        avg_exh += val
    avg_exh /= len(exhaust_times)
    print("Avg. Exhaustive Search Time: %s" % avg_exh)
    
    top_ratio = avg_exh / avg_top
    astar_ratio = avg_exh / avg_astar
    astar_top_ratio = avg_top / avg_astar
    print('\nResults Summary:')
    print('---------------------------------------------------------------------------')
    print("On average, TO outperforms EXH by: %s times" % top_ratio)
    print("On average, A* outperforms EXH by: %s times" % astar_ratio)
    print("On average, A* outperforms TO by: %s times" % astar_top_ratio)
    
main()