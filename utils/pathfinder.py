def createDAG(train_array, player, walls, start, finish):
    dir_graph = {}
    count, maxIterations = 0, len(train_array) * len(train_array[0])
    while (count := count + 1) <= maxIterations:
        curr_x, curr_y = int(player.rect.x / 18) + 1, int(player.rect.y / 18) + 1
        curr_xy = (curr_x, curr_y)
        if dir_graph.get(curr_xy, None) == None:    dir_graph[(curr_x, curr_y)] = {}
        player.generateDirectedAcyclicGraph(dir_graph, player, train_array, walls, curr_xy)
    
    start_xy = (int(start[0] / 18), int(start[1] / 18))
    finish_xy = (int(finish[0] / 18), int(finish[1] / 18))
    path = find_path(dir_graph, start_xy, finish_xy)
    return path

def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:    return path
    if graph.get(start, {}) == {}:  return []
    
    for node in graph[start]:
        if graph[start][node] not in path:
            newpath = find_path(graph, graph[start][node], end, path)
            if newpath: return newpath
              
    return []