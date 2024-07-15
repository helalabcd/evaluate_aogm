import numpy as np
import networkx as nx
from scipy.optimize import linear_sum_assignment

def pad_adjacency_matrix(adj_matrix, target_size):
    current_size = adj_matrix.shape[0]
    if current_size == target_size:
        return adj_matrix
    padded_matrix = np.zeros((target_size, target_size))
    padded_matrix[:current_size, :current_size] = adj_matrix
    return padded_matrix

def calculate_cost_matrix(G1, G2):
    nodes1 = list(G1.nodes)
    nodes2 = list(G2.nodes)
    n1 = len(nodes1)
    n2 = len(nodes2)
    size = max(n1, n2)
    
    cost_matrix = np.full((size, size), fill_value=1000)  # Initialize with high cost for unmatched nodes

    adj_matrix1 = pad_adjacency_matrix(nx.adjacency_matrix(G1).todense(), size)
    adj_matrix2 = pad_adjacency_matrix(nx.adjacency_matrix(G2).todense(), size)

    for i in range(n1):
        for j in range(n2):
            feature_cost = np.linalg.norm(np.array(G1.nodes[nodes1[i]].get('x', [0])) - np.array(G2.nodes[nodes2[j]].get('x', [0])))
            feature_cost += np.linalg.norm(np.array(G1.nodes[nodes1[i]].get('y', [0])) - np.array(G2.nodes[nodes2[j]].get('y', [0])))
            feature_cost += np.linalg.norm(np.array(G1.nodes[nodes1[i]].get('t', [0])) - np.array(G2.nodes[nodes2[j]].get('t', [0])))
            edge_cost = np.linalg.norm(adj_matrix1[i] - adj_matrix2[j])
            cost_matrix[i][j] = feature_cost + edge_cost

    return cost_matrix

def calculate_AOGM(G1, G2):
    cost_matrix = calculate_cost_matrix(G1, G2)
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    total_cost = cost_matrix[row_ind, col_ind].sum()
    aogm = total_cost / max(len(G1.nodes), len(G2.nodes))
    return aogm
