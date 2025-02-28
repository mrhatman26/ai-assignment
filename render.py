import matplotlib.pyplot as plt
import numpy as np 
from setup import clean_normalise_boolean_to_int
from misc import *

def render_scatter_dataset(dataset, dataset_name, show_graph):
    try:
        x = dataset[dataset_name].drop(columns="rating")
        y = dataset["rating"].drop(columns=dataset_name)
        x = np.array(list(x), dtype=int)
        y = np.array(list(y), dtype=int)
        if x.shape != y.shape:
            x = clean_normalise_boolean_to_int(dataset, dataset_name)
            x = np.array(list(x[dataset_name]), dtype=int)
        if show_graph is True:
            plt.scatter(x, y)
        plt.savefig("./saved_data/graphs/original_" + dataset_name + ".png")
    except Exception as e:
        error_exit(e)