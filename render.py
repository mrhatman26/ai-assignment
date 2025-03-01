import matplotlib.pyplot as plt
import numpy as np 
import ast
from setup import clean_normalise_boolean_to_int
from misc import *

def render_scatter_int(dataset, dataset_name, show_graph, xlabel, title):
    print("Adding rows to the scattergraph...", end="")
    try:
        for i in range(0, len(dataset)):
            x = np.array(dataset[dataset_name][i])
            y = np.array(dataset["rating"][i])
            plt.scatter(x, y)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("User Rating (0-10)")
        if show_graph is True:
            plt.show()
        plt.savefig("./saved_data/graphs/integer_" + dataset_name + ".png")
        plt.close()
        print("Done.")
    except Exception as e:
        error_exit(e)

def render_scatter_bool(dataset, dataset_name, show_graph, xlabel, title, show_legend=True):
    try:
        map_file = load_dataset_map(dataset_name, True)
        map_file_original = load_dataset_map(dataset_name)
        print("Plotting " + dataset_name + " boolean values on scatter graph...", end="")
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel("User Rating (0-10)")
        gca = plt.gca()
        pattern = 1
        for item in map_file:
            x = []
            y = []
            for i in range(0, len(dataset)):
                row = dataset[dataset_name][i]
                if str(row) == item:
                    x.append(item)
                    y.append(dataset["rating"][i])
            x = np.array(x)
            gca.axes.get_xaxis().set_ticks([]) #Prevent X Axis from showing EVERY element.
            y = np.array(y)
            if show_legend is True:
                plt.scatter(x, y, label=str(map_file_original[pattern - 1]))
                plt.legend()
            else:
                plt.scatter(x, y)
            pattern += 1
        if show_graph is True:
            plt.show()
        plt.savefig("./saved_data/graphs/boolean_" + dataset_name + ".png")
        plt.close()
        print("Done.")        
    except Exception as e:
        error_exit(e)