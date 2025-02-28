import matplotlib.pyplot as plt
import numpy as np 
import ast
from setup import clean_normalise_boolean_to_int
from misc import *

def render_scatter_int(dataset, dataset_name, show_graph, xlabel, title):
    dataset.to_csv('./saved_data/youareanutterfailureyouretard_' + dataset_name + ".csv")
    try:
        for i in range(0, len(dataset)):
            print(str(i + 1) + " of " + str(len(dataset)) + " rows added to scatter graph for " + dataset_name, end="\r")
            x = np.array(dataset[dataset_name][i])
            y = np.array(dataset["rating"][i])
            plt.scatter(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("User Rating (0-10)")
        if show_graph is True:
            plt.show()
        plt.savefig("./saved_data/graphs/original_" + dataset_name + ".png")
        plt.close()
    except Exception as e:
        error_exit(e)

def render_scatter_bool(dataset, dataset_name, show_graph, xlabel, title):
    pass
    #To handle mapping... Somehow... Good luck. -_-