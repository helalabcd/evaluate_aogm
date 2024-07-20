from .helpers import digraph_from_bust
from .aogm import digraph_from_bust


def calculate_aogm(model):

    aogms = []
    for burst in os.listdir("data/validation"):
    
        images = [Image.open(f"data/validation/{burst}/img1/" + x) for x in sorted(os.listdir(f"data/validation/{burst}/img1/"))]
        predicted_graph = model.forward_inference(images)
    
        label_graph = digraph_from_bust(burst)
        aogm = calculate_AOGM(label_graph, predicted_graph)
        aogms.append(aogm)
        print("AOGM", aogm)
    
