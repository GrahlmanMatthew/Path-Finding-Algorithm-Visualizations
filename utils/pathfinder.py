import copy 

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:    return path
    if graph.get(start, {}) == {}:  return []
    
    for node in graph[start]:
        if graph[start][node] not in path:
            newpath = find_path(graph, graph[start][node], end, path)
            if newpath: return newpath
              
    return []

def createTopoDAG(train_array, player, walls, start, finish):
    t_array = copy.deepcopy(train_array)
    dir_graph = {}
    count, maxIterations = 0, len(t_array) * len(t_array[0]) 
    while (count := count + 1) <= maxIterations:
        curr_x, curr_y = int(player.rect.x / 18) + 1, int(player.rect.y / 18) + 1
        curr_xy = (curr_x, curr_y)
        if dir_graph.get(curr_xy, None) == None:    dir_graph[(curr_x, curr_y)] = {}
        player.generateDirectedAcyclicGraph(dir_graph, player, t_array, walls, curr_xy)
    start_xy = (int(start[0] / 18), int(start[1] / 18))
    finish_xy = (int(finish[0] / 18), int(finish[1] / 18))
    path = find_path(dir_graph, start_xy, finish_xy)    
    return path

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:    return [path]
    if graph.get(start, {}) == {}:  return []
    
    paths = []
    for node in graph[start]:
        if node not in path: 
            newpaths = find_all_paths(graph, node, end, path)
            for np in newpaths:
                paths.append(np)     
    return paths

def createAStarGraph(train_array, player, walls, start, finish):
    t_array = copy.deepcopy(train_array)
    start_xy = (int(start[0] / 18), int(start[1] / 18))
    finish_xy = (int(finish[0] / 18), int(finish[1] / 18))
    
    dag = {}
    queue = [start_xy]    
    while queue:
        curr_x, curr_y = queue.pop(0)
        edges = dag[(curr_x, curr_y)] = []
        
        coords = [
            (curr_x-1, curr_y),
            (curr_x, curr_y-1),
            (curr_x, curr_y+1),
            (curr_x+1, curr_y)
        ]
        
        for coord in coords:
            if coord in dag.keys(): continue    # visited before
            node_val = t_array[coord[1]][coord[0]]
            
            if node_val == " ":
                edges.append(coord)
                queue.append(coord)
            
            if node_val == 'E':
                edges.append(coord)
        
    allpaths = find_all_paths(dag, start_xy, finish_xy)
    return allpaths