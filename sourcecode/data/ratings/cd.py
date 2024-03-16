import networkx as nx
import pandas as pd
from community import community_louvain
import random
import glob

# Use glob to find all files matching the pattern
file_list = glob.glob('./ratings-*.tsv')

# Load and concatenate the data from all matching files
df_list = [pd.read_csv(file, sep='\t', usecols=['noteId', 'raterParticipantId']) for file in file_list]
df = pd.concat(df_list, ignore_index=True)

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'raterParticipantId', 'noteId', create_using=nx.Graph())

# Detect communities
partition = community_louvain.best_partition(G)

# Calculate and print the modularity of the entire network
modularity_score = community_louvain.modularity(partition, G)
print(f"Modularity Score: {modularity_score}")

# Precompute degrees for all nodes (if needed for your version of conductance calculation)
# node_degrees = dict(G.degree())

# Iterate over communities and calculate simplified conductance
for community in set(partition.values()):
    # Extract nodes in the current community
    nodes_in_community = [node for node in partition if partition[node] == community]
    community_subgraph = G.subgraph(nodes_in_community)
    
    # Use nx.edge_boundary for a more efficient boundary edge calculation
    boundary_edges = nx.edge_boundary(G, nodes_in_community)
    cut_size = len(boundary_edges)
    
    # Simplified demonstration of conductance calculation
    # You can replace these calculations with more accurate ones as needed
    conductance = cut_size / len(community_subgraph.edges()) if community_subgraph.edges() else 0
    
    print(f"Community {community}: Conductance = {conductance}")
