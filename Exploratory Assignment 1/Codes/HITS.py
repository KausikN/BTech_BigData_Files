'''
HITS
Hyperlink Induced Topic Search Algorithm Implementation
'''

# Imports
import networkx as nx
import matplotlib.pyplot as plt

# Main Functions
def HITS_Library(Edges, max_iters=10, normalized=True, displayGraph=True):
    Graph = nx.DiGraph()
    Graph.add_edges_from(Edges)

    if displayGraph:
        plt.figure(figsize =(10, 10))
        nx.draw_networkx(Graph, with_labels = True)
        plt.show()

    hubs, authorities = nx.hits(Graph, max_iter=max_iters, normalized=normalized)
    # The in-built hits function returns two dictionaries keyed by nodes
    # containing hub scores and authority scores respectively.

    return hubs, authorities

def HITS(Edges, max_iters=10, normalized=True, displayGraph=True):
    AdjMatrix, Nodes = GetAdjacencyMatrix(Edges)

    # Init
    hubs = {}
    authorities = {}
    for n in Nodes:
        hubs[n] = 1
        authorities[n] = 1

    if displayGraph:
        Graph = nx.DiGraph()
        Graph.add_edges_from(Edges)
        plt.figure(figsize =(10, 10))
        nx.draw_networkx(Graph, with_labels = True)
        plt.show()

    # Iters
    for it in range(max_iters):
        # Evaluate Hub Scores and Authority Scores
        for i in range(len(Nodes)):
            new_score_hub = 0
            new_score_authority = 0
            for j in range(len(AdjMatrix)):
                if AdjMatrix[i][j]:
                    new_score_hub += authorities[Nodes[j]]
                if AdjMatrix[j][i]:
                    new_score_authority += hubs[Nodes[j]]
            hubs[Nodes[i]] = new_score_hub
            authorities[Nodes[i]] = new_score_authority
        # Normalise
        if normalized:
            hubs = Normalise(hubs)
            authorities = Normalise(authorities)
    
    return hubs, authorities


def GetAdjacencyMatrix(Edges):
    Nodes = []
    for edge in Edges:
        if not edge[0] in Nodes:
            Nodes.append(edge[0])
        if not edge[1] in Nodes:
            Nodes.append(edge[1])
    AdjMatrix = []
    for i in range(len(Nodes)):
        row = []
        for j in range(len(Nodes)):
            if i == j:
                row.append(False)
            elif (Nodes[i], Nodes[j]) in Edges:
                row.append(True)
            else:
                row.append(False)
        AdjMatrix.append(row)
    return AdjMatrix, Nodes

def Normalise(arr):
    arr_norm = {}
    sumsquares = 0
    for ak in arr.keys():
        sumsquares += arr[ak] ** 2
    sumsquares = sumsquares ** (0.5)
    for ak in arr.keys():
        arr_norm[ak] = arr[ak] / sumsquares
    return arr_norm


# Driver Code
Edges = [   ('A', 'D'), ('B', 'C'), ('B', 'E'), ('C', 'A'),
            ('D', 'C'), ('E', 'D'), ('E', 'B'), ('E', 'F'),
            ('E', 'C'), ('F', 'C'), ('F', 'H'), ('G', 'A'),
            ('G', 'C'), ('H', 'A')
        ]
max_iterations = 100
normalized = True

displayGraph = False

hubs_lib, authorities_lib = HITS_Library(Edges, max_iters=max_iterations, normalized=normalized, displayGraph=displayGraph)
hubs, authorities = HITS(Edges, max_iters=max_iterations, normalized=normalized, displayGraph=displayGraph)

print("Self Implementation:")
print("Hub Scores: ")
for key in hubs.keys():
    print(key + ":", hubs[key])
print("\n")
print("Authority Scores: ")
for key in authorities.keys():
    print(key + ":", authorities[key])

print("\n\n")

print("Library Implementation:")
print("Hub Scores: ")
for key in hubs_lib.keys():
    print(key + ":", hubs_lib[key])
print("\n")
print("Authority Scores: ")
for key in authorities_lib.keys():
    print(key + ":", authorities_lib[key])