import pandas as pd
from setup import *
from create_knn import KNNCreator
from create_linear import LinearCreator
from render import *
from misc import *
check_save_dir_exists() #Check if ./saved_data/ exists. If it does not, create it.
pd.options.mode.chained_assignment = None 
pd.set_option('display.max_columns', None) #Allows for ALL columns to be printed.
pd.set_option('display.max_rows', None) #Allows for ALL rows to be printed.
#Load CSV file using Pandas.
print("Loading dataset...", end="")
try:
    original_dataset = pd.read_csv("IMDb Movies Dataset.csv")
except Exception as e:
    error_exit(e)
print("Done")
#Clean dataset and split into four datasets.
cleaned_dataset = clean_remove_unused(original_dataset)
age_rating_dataset = clean_remove_other_columns(cleaned_dataset, "movie_rated")
runtime_dataset = clean_remove_other_columns(cleaned_dataset, "run_length")
genres_dataset = clean_remove_other_columns(cleaned_dataset, "genres")
date_dataset = clean_remove_other_columns(cleaned_dataset, "release_date")
#Normalise the four datasets.
knn_age_rating_dataset = clean_normalise_boolean(age_rating_dataset, "movie_rated") #Normalise age rating column as Boolean values
linear_age_rating_dataset = clean_normalise_boolean_to_int(knn_age_rating_dataset.copy(), "movie_rated")
knn_runtime_dataset = clean_normalise_runtime(runtime_dataset)#Normalise runtime length column as integers.
linear_runtime_dataset = knn_runtime_dataset.copy()
knn_genres_dataset = clean_normalise_boolean(genres_dataset, "genres", "; ") #Normalise genres column as Boolean values.
linear_genres_dataset = clean_normalise_boolean_to_int(knn_genres_dataset.copy(), "genres")
knn_date_dataset = clean_normalise_months(date_dataset) #Normalise release date column as integers.
linear_date_dataset = knn_date_dataset.copy()
#Create the models from the dataset.
print("\n**Creating KNN Models**")
knn_age_classifier = KNNCreator(knn_age_rating_dataset, "movie_rated")
knn_length_classifier = KNNCreator(knn_runtime_dataset, "run_length")
knn_genre_classifier = KNNCreator(knn_genres_dataset, "genres")
knn_date_classifier = KNNCreator(knn_date_dataset, "release_date")
knn_classifiers = [knn_age_classifier, knn_length_classifier, knn_genre_classifier, knn_date_classifier] #For simplicity
print("\n**Creating Lineaer Regression Models**")
linear_age_classifier = LinearCreator(linear_age_rating_dataset, "movie_rated")
linear_length_classifier = LinearCreator(linear_runtime_dataset, "run_length")
linear_genre_classifier = LinearCreator(linear_genres_dataset, "genres")
linear_date_classifier = LinearCreator(linear_date_dataset, "release_date")
linear_classifiers = [linear_age_classifier, linear_length_classifier, linear_genre_classifier, linear_date_classifier]
#Run the KNN classifier.
print("\n**Running KNNCreator Methods**")
for classifier in knn_classifiers:
    print("---------------------------------------------------------------------")
    classifier.classifier_init() #Start the classifier (Setting up the data by splitting it into training and testing).
    classifier.generate_confusion_matrix() #Generate confusion matrix for a visual representation of the accuracy of the model.
    classifier.train_kfold() #Train the model using KFOLD.
    classifier.save_model() #Save the model using pickle.
    print("---------------------------------------------------------------------\n")
#Run the Linear Regression classifier.
for classifier in linear_classifiers:
    print("---------------------------------------------------------------------")
    classifier.linear_init()
    classifier.generate_confusion_matrix()
    classifier.save_model()
    print("---------------------------------------------------------------------\n")
print("\n**Generating graphs**")
show_graphs = ask_question("Would you like for the graphs to be shown after generating them?")
#Datasets Graphs
#KNN
#Render scatter graphs of the KNN data
render_scatter_bool(knn_age_rating_dataset, "movie_rated", show_graphs, "Age Rating", "User Ratings of Age Ratings", "knn")
render_scatter_int(knn_runtime_dataset, "run_length", show_graphs, "Runtime (Minutes)", "User Ratings of Runtime", "knn")
render_scatter_bool(knn_genres_dataset, "genres", show_graphs, "Genres", "User Ratings of Genres", "knn", False)
render_scatter_int(knn_date_dataset, "release_date", show_graphs, "Release Month", "User Ratings of Release Month", "knn")
#Render bar charts of the knn classification reports
render_classification_bar("movie_rated", show_graphs, knn_age_classifier, "knn")
render_classification_bar("run_length", show_graphs, knn_length_classifier, "knn")
render_classification_bar("genres", show_graphs, knn_genre_classifier, "knn")
render_classification_bar("release_date", show_graphs, knn_date_classifier, "knn")
#Linear
#Render scatter graphs of the linear data
render_scatter_int(linear_age_rating_dataset, "movie_rated", show_graphs, "Age Rating", "User Ratings of Age Ratings", "linear")
render_scatter_int(linear_runtime_dataset, "run_length", show_graphs, "Runtime (Minutes)", "User Ratings of Runtime", "linear")
render_scatter_int(linear_genres_dataset, "genres", show_graphs, "Genres", "User Ratings of Genres", "linear")
render_scatter_int(linear_date_dataset, "release_date", show_graphs, "Release Month", "User Ratings of Release Month", "linear")
#Render bar charts of the linear classification reports
render_classification_bar("movie_rated", show_graphs, linear_age_classifier, "linear")
render_classification_bar("run_length", show_graphs, linear_length_classifier, "linear")
render_classification_bar("genres", show_graphs, linear_genre_classifier, "linear")
render_classification_bar("release_date", show_graphs, linear_date_classifier, "linear")
#KNN Heatmaps
#Generate heatmaps from the knn confusion matrixes
for classifier in knn_classifiers:
    render_heatmap(classifier, classifier.dataset_name, show_graphs, "knn")
#Linear Heatmaps
#Generate heatmaps from the linear confusion matrixes
for classifier in linear_classifiers:
    render_heatmap(classifier, classifier.dataset_name, show_graphs, "linear")
print("\n**Model Generation Finished**")
pause(True)