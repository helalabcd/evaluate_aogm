from .helpers import digraph_from_bust
from .aogm import calculate_AOGM

from PIL import Image
import os

def calculate_aogm(model):

    aogms = []
    for burst in os.listdir("HeLa_dataset/test"):
    
        images = [Image.open(f"HeLa_dataset/test/{burst}/img1/" + x) for x in sorted(os.listdir(f"HeLa_dataset/test/{burst}/img1/"))]
        predicted_graph = model.forward_inference(images)
    
        label_graph = digraph_from_bust(burst)
        aogm = calculate_AOGM(label_graph, predicted_graph)
        aogms.append(aogm)
        print("AOGM", aogm)
    
