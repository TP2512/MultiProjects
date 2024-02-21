from Graph_Processing import logger

def bfs(graph ,node, visited=None):
    if not visited:
        visited = []
        visited.append(node)
        queue = []
        queue.append(node)
    while queue:
        sn = queue.pop(0)
        for neighbour in graph[sn]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    logger.info(f"got bfs request on graph with node: {node} --> bfs is\n --> {visited}")
    return visited

def dfs(graph, node, visited=None):
    if not visited:
        visited = []

    visited.append(node)
    for neighbour in graph[node]:
        if neighbour not in visited:
            dfs(graph, neighbour, visited)
    return visited




