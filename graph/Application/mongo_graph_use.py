from pymongo import MongoClient
from Graph_Processing.graph_creation import Graphs
from Graph_Processing.analyze_graph import bfs,dfs

db_name="my_graph_database"
CONNECTION_STRING = "mongodb://localhost:27017"
client = MongoClient(CONNECTION_STRING)
db=client[db_name]
collections = db.list_collection_names()   #list all collections in db
print(f"All collections in db: {db_name} are: \n {collections}")

edges_data = db.edges.find({},{'_id':0})
edges = [(edge["source"], edge["target"]) for edge in edges_data]
print(edges)

g1=Graphs()
g1.add_edges(edges)

# g2=Graphs()
# g2.add_edges(edges)
print(len(g1))
print(g1)

# print(len(g2))
# print(g2)

print("BFS path of graph1:",bfs(g1,'a'))
print("DFS path of graph1:",dfs(g1,'a'))

print("BFS path of graph1:",bfs(g1,'b'))
print("DFS path of graph1:",dfs(g1,'c'))