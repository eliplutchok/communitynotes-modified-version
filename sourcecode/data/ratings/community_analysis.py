import networkx as nx
import pandas as pd
from community import community_louvain
import random
import glob

# Adjust the path to your data source to include the directory and the pattern
path_to_files = './ratings-*.tsv'  # Assuming the files are in the current directory

# Use glob to find all files matching the pattern
file_list = glob.glob(path_to_files)

# Load and concatenate the data from all matching files
df_list = [pd.read_csv(file, sep='\t', usecols=['noteId', 'raterParticipantId']) for file in file_list]
df = pd.concat(df_list, ignore_index=True)

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'raterParticipantId', 'noteId', create_using=nx.Graph())

# Detect communities
partition = community_louvain.best_partition(G)

# Basic analysis of the resulting communities
# Count the number of nodes in each community
community_sizes = {}
for node, comm in partition.items():
    if comm not in community_sizes:
        community_sizes[comm] = 0
    community_sizes[comm] += 1

# Print the total amount of communities
print(f"Total communities detected: {len(community_sizes)}")

# Filter communities with more than 5,000 nodes
large_communities = {comm: size for comm, size in community_sizes.items() if size > 5000}

# Print the size of each large community and 5 random noteIds from each community
for comm, size in large_communities.items():
    print(f"Community {comm} has {size} nodes.")
    
    # Find noteIds in this community
    notes_in_community = [node for node, community in partition.items() if community == comm]
    
    # Select 5 random noteIds (or all if there are less than 5)
    random_notes = random.sample(notes_in_community, min(len(notes_in_community), 5))
    
    print(f"5 random noteIds from Community {comm}: {random_notes}")
