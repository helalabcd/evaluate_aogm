from .helpers import digraph_from_bust, plot_sequence
from .aogm import calculate_AOGM

from PIL import Image
import os
from tqdm import tqdm
import networkx as nx

def calculate_aogm(model, mode="first", plot_tracking_sequences=True, filename_prefix="no_prefix"):

    # mode can be "first" or "full"
    
    model.configure_inference()

    aogms = []
    for burst in tqdm(sorted(os.listdir("HeLa_dataset/test"))):
    
        images = [Image.open(f"HeLa_dataset/test/{burst}/img1/" + x) for x in sorted(os.listdir(f"HeLa_dataset/test/{burst}/img1/"))]
        predicted_graph = model.forward_inference(images)
    
        label_graph = digraph_from_bust(burst)
        aogm = calculate_AOGM(label_graph, predicted_graph)
        aogms.append(aogm)

        if plot_tracking_sequences:
            print("Plotting sequence")
            os.system("mkdir plotting")
            plot_sequence("HeLa_dataset/test/" + burst, predicted_graph, f"plotting/{filename_prefix}/{burst}.png")

        if mode == "first":
            return aogm
    return sum(aogms) / len(aogms)    

def calculate_edit_distance(model, mode="first"):

    # mode can be "first" or "full"
    
    model.configure_inference()

    eds = []
    for burst in tqdm(sorted(os.listdir("HeLa_dataset/test"))):
    
        images = [Image.open(f"HeLa_dataset/test/{burst}/img1/" + x) for x in sorted(os.listdir(f"HeLa_dataset/test/{burst}/img1/"))]
        predicted_graph = model.forward_inference(images)
    
        label_graph = digraph_from_bust(burst)
        ed = nx.graph_edit_distance(label_graph, predicted_graph)
        eds.append(ed)

        if mode == "first":
            return ed
    return sum(eds) / len(eds)    
