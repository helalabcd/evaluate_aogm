import os
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import math

def plot_sequence(burst, g):
    frames = os.listdir("Burst4_A2_1_VesselID-29_1-0/img1/")
    frames = [x for x in frames if x.endswith(".tiff")]
    frames = sorted(frames)
    frames = ["Burst4_A2_1_VesselID-29_1-0/img1/" + x for x in frames]

    side = int(math.sqrt(len(frames))) + 1
    fig, ax = plt.subplots(side, side, figsize=(50,50))

    for idx, frame in enumerate(frames):
        idx += 1
        ax.flat[idx-1].imshow(Image.open(frame))

    for n in g.nodes:
        t = g.nodes[n]["t"]
        x = g.nodes[n]["x"]
        y = g.nodes[n]["y"]
        ax.flat[t-1].scatter([x], [y])
    plt.savefig("output.png")

def digraph_from_bust(burst):
    burst = "HeLa_dataset/test/" + burst

    frames = sorted(os.listdir(burst + "/img1/"))
    frames = [burst + "/img1/" + x for x in frames]

    graph = nx.DiGraph()
    data = pd.read_csv(burst + "/gt/gt.txt", names=["t", "cell_id", "a", "b", "c", "d", "co", "cc", "ccc", "cccc"])
    
    last_mapping = None
    
    graph_idx = 0
    # Iterate over frames
    for i in range(data["t"].max()):
        i+=1
        framedata = data[data["t"] == i]
        
        cf = frames[i-1]
        #plt.imshow(Image.open(cf))

        current_mapping = {}
        for i, row in framedata.iterrows():
            
            #plt.scatter([row.a + (row.c // 2)], [row.b + (row.d // 2)])
            x = row.a + (row.c // 2)
            y = row.b + (row.d // 2)
            int_cell_id = int(row.cell_id)
            
            attributes = {'t': int(row.t), 'x': int(x.item()), 'y': int(y.item())}
            graph.add_node(graph_idx, **attributes)
            current_mapping[int_cell_id] = graph_idx
            
            if last_mapping is not None and int_cell_id in last_mapping.keys():
                # Draw edge pointing to previous node of same cell_id
                graph.add_edge(graph_idx, last_mapping[int_cell_id])
            
            graph_idx += 1
        
        last_mapping = current_mapping
        
        #plt.show()
        #plt.close()
        
    return graph

def get_sha256_first5(input_string):
    # Encode the input string to bytes
    encoded_string = input_string.encode()

    # Create a SHA-256 hash object
    sha256_hash = hashlib.sha256(encoded_string)

    # Get the hexadecimal digest of the hash
    hex_digest = sha256_hash.hexdigest()

    # Return the first 5 characters of the hex digest
    return hex_digest[:5]

