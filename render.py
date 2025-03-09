import matplotlib.pyplot as plt
import numpy as np 
import seaborn
from misc import *
from file_paths import *

def render_scatter_int(dataset, dataset_name, show_graph, x_label, title, classifier):
    #Creates a scatter graph from the entered dataset and saves it to the graphs folder in saved_data.
    print("Adding rows to the scattergraph...", end="")
    try:
        for i in range(0, len(dataset)):
            #For every row of the dataset, add the current row's rating and dataset_name values to the scattergraph.
            x = np.array(dataset[dataset_name][i])
            y = np.array(dataset["rating"][i])
            plt.scatter(x, y)
        plt.title(title) #Title the graph.
        plt.xlabel(x_label) #Set the X axis' title.
        plt.ylabel("User Rating (0-10)") #Set the Y axis' title.
        #If the user asked to see the graph, it will be shown to them, if not, it is skipped.
        if show_graph is True:
            plt.show()
        #Save the graph to the saved_data graphs directory with the name of its classifer followed by "_integer_", it's dataset name and then finally ".png".
        plt.savefig(saved_graphs_dir + classifier + "_integer_" + dataset_name + ".png")
        plt.close()
        print("Done.")
    except Exception as e:
        error_exit(e)

def render_scatter_bool(dataset, dataset_name, show_graph, x_label, title, classifier, show_legend=True):
    #The same as the last function, but it takes boolean values rather than integers.
    try:
        map_file = load_dataset_map(dataset_name, True)
        map_file_original = load_dataset_map(dataset_name)
        print("Plotting " + dataset_name + " boolean values on scatter graph...", end="")
        plt.title(title)
        plt.xlabel(x_label)
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
        plt.savefig(saved_graphs_dir + classifier + "_boolean_" + dataset_name + ".png")
        plt.close()
        print("Done.")        
    except Exception as e:
        error_exit(e)

def render_heatmap(model, dataset_name, show_graph, classifier):
    #Generates a heatmap of dataset using the seaborn library.
    try:
        print("Creating a heatmap from " + dataset_name + "...", end="")
        heatmap = seaborn.heatmap(model.confusion, annot=True, cmap='nipy_spectral_r')
        if show_graph is True:
            heatmap.figure.show()
        heatmap.figure.savefig(saved_graphs_dir + classifier + "_heatmap_" + dataset_name + ".png")
        plt.close()
        print("Done.")
    except Exception as e:
        error_exit(e)

def render_classification_bar(dataset_name, show_graph, classifier, classifer_name):
    #Generates a bar chart of the classifcation report from teh classifier.
    try:
        print("Creating a bar chart for the " + dataset_name + " model's classification report...", end="")
        for key, value in classifier.class_report_dict.items():
            if "accuracy" not in key:
                for alt_key, alt_value in value.items():
                    if "support" not in alt_key:
                        plt.bar(alt_key, alt_value, 0.2, label=alt_key.title())
            else:
                pass
            plt.legend()
            plt.xlabel("Stats")
            plt.ylabel("Score")
            if show_graph is True:
                plt.show()
            plt.savefig(saved_graphs_dir + classifer_name + "_" + dataset_name + "_bar_" + str(key) + ".png")
            plt.close()
        print("Done.")
    except Exception as e:
        error_exit(e)