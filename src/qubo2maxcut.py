"""
    Solve TSP by transforming into a QUBO problem and reducing it to MaxCut.

    Uses nodes for the QUBO formulation.
    Assumes graph is completely connected and weights are plain distances.
    Unconnected edges or more complex weights would require formulation around edges.
"""
import numpy as np
from itertools import product
import networkx as nx
import qaoa_maxcut

"""
From distances between points, build graph for MaxCut.

Args:
    - dists (2d np.array): symmetric adjacency matrix
        dists[i,j] = distance(i,j)

Returns:
    - nx.Graph: graph for MaxCut
"""
def qubo2maxcut(dists):
    N = len(dists)
    max_dist = np.max(dists)

    # QUBO parameters 
    # A > B * N * max(distance)
    B = 1
    A = (B * N * max_dist)

    # QUBO coefficients
    q = np.zeros((N*N, N*N))
    for i, j, k, l in product(range(N), repeat=4):
        x = i*N + k
        y = j*N + l
        if x == y:
            q[x,y] -= 4*A
        if i == j:
            q[x,y] += A
        if k == l:
            q[x,y] += A
        if k+1 == l:
            q[x,y] += B*dists[i,j]
    print(q)
    
    # MaxCut weights
    graph = nx.Graph()
    for j in range(N*N):
        # Remove diagonal from the sum!
        a = np.sum(q[:,j])
        b = np.sum(q[j,:])
        graph.add_edge(0, j+1, weight=a+b)
    for i in range(N*N):
        for j in range(0, i):
            graph.add_edge(i+1, j+1, weight=q[i,j]+q[j,i])
    return graph


if __name__ == "__main__":
    N = 4
    nodes = np.random.rand(N, 2) * 10  # Random nodes
    matrix = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            matrix[i, j] = np.linalg.norm(nodes[i] - nodes[j])

    matrix = np.zeros((4,4))
    matrix += 0.1
    matrix[0,1] = matrix[1,0] = 1
    matrix[0,2] = matrix[2,0] = 1
    matrix[1,3] = matrix[3,1] = 1
    matrix[2,3] = matrix[3,2] = 1

    matrix = np.ones((2,2))

    graph = qubo2maxcut(matrix)
    #print(graph.edges(data="weight"))
    res = qaoa_maxcut.run_qaoa_maxcut(graph, 8)
    print(res)
