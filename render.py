import matplotlib.pyplot as plt
import numpy as np 
import ast
from setup import clean_normalise_boolean_to_int
from misc import *

def render_scatter_dataset_old(dataset, dataset_name, show_graph, xlabel):
    try:
        x = dataset[dataset_name].drop(columns="rating")
        y = dataset["rating"].drop(columns=dataset_name)
        x = np.array(list(x), dtype=int)
        y = np.array(list(y), dtype=int)
        if x.shape != y.shape:
            x = clean_normalise_boolean_to_int(dataset, dataset_name)
            x = np.array(list(x[dataset_name]), dtype=int)
        plt.xlabel(xlabel)
        plt.ylabel("User Rating")
        if show_graph is True:
            plt.scatter(x, y)
        plt.savefig("./saved_data/graphs/original_" + dataset_name + ".png")
    except Exception as e:
        error_exit(e)

def render_scatter(dataset, dataset_name, show_graph, xlabel, title):
    try:
        dataset_map = load_dataset_map(dataset_name, check_list_bool(dataset[dataset_name][0]))
        for i in range(0, len(dataset)):
            print(str(i + 1) + " of " + str(len(dataset)) + " rows added to scatter graph for " + dataset_name, end="\r")
            if dataset_name == "genres":
                print(dataset_map.index(str(dataset[dataset_name][i])))
                x = np.array(dataset_map.index(str(dataset[dataset_name][i])))
            else:
                x = np.array(dataset[dataset_name][i])
            y = np.array(dataset["rating"][i])
            plt.scatter(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("User Rating (0-10)")
        if show_graph is True:
            plt.show()
        plt.savefig("./saved_data/graphs/original_" + dataset_name + ".png")
    except Exception as e:
        error_exit(e)