from Graph_Processing import logger


class Graphs:
    """This is bidirectional graph containing nodes and edges"""
    def __init__(self):
        self.Graph= {}


    def add_node(self, node):
        # logger.debug(f"Added node: {node}")
        if node not in self.Graph:
            self.Graph[node]=set()



    def add_edges(self,edge_list):
        for i in edge_list:
            logger.debug(f"Added edge from list {i}")
            self.add_edge(*i)



    def add_edge(self, source, target):
        if source not in self.Graph:
            self.Graph[source]=set()
        if target not in self.Graph:
            self.Graph[target]=set()
        if source in self.Graph:
            self.Graph[source].add(target)
        if target in self.Graph:
            self.Graph[target].add(source)
        logger.debug(f"Added edge: {source} -> {target} and  {source} <- {target}")


    def __getitem__(self, node):
        logger.info(f"Requested for node details: {node}")
        return self.Graph.get(node)


    def __str__(self) -> str:
        return str(self.Graph)


    def __len__(self):
        return len(self.Graph)


    def __iter__(self):
        return iter(self.Graph.keys())


    def remove_node(self,node: str):
        try:
            for item in self.Graph:
                if node in self.Graph[item]:
                    self.Graph[item].remove(node)
            del self.Graph[node]
        except KeyError:
            raise Exception(f"node '{node}' not found")


    def remove_edge(self,edge: tuple):
        if edge[0] in self.Graph:
            self.Graph[edge[0]].remove(edge[1])
            self.Graph[edge[1]].remove(edge[0])


if __name__=="__main__":
    g1=Graphs()
    g1.add_node('AA')
    g1.add_node('AB')
    g1.add_edge('A', 'B')
    g1.add_edge('B', 'F')
    g1.add_edge('F', 'G')
    g1.add_edge('G', 'H')
    g1.add_edge('A', 'H')
    g1.add_edge('H', 'K')
    print("Graph Details:",g1)
    # print("BFS path of graph: ",g1.bfs('A'))
    print("DFS path of graph: ", g1.dfs('A'))
    print("adjecency list of node 'A':",g1['A'])
    print("no of nodes in graph: ",len(g1))
    print(g1.__doc__)
    g1.remove_node('H')
    g1.remove_edge(('G','F'))
    print("Graph Details:", g1)
    for node in g1:
        print(node,end=" ")
    g1.remove_edge(('O','P'))
    # g1.remove_node('L')


