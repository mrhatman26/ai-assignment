import pandas as pd
from setup import *
from create import KNNCreator
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
age_rating_dataset = clean_normalise_boolean(age_rating_dataset, "movie_rated") #Normalise age rating column as Boolean values
runtime_dataset =  clean_normalise_runtime(runtime_dataset)#Normalise runtime length column as integers.
genres_dataset = clean_normalise_boolean(genres_dataset, "genres", "; ") #Normalise genres column as Boolean values.
date_dataset = clean_normalise_months(date_dataset) #Normalise release date column as integers.
#Create the models from the dataset.
print("\n**Creating KNN Models**")
age_classifier = KNNCreator(age_rating_dataset, "movie_rated")
length_classifier = KNNCreator(runtime_dataset, "run_length")
genre_classifier = KNNCreator(genres_dataset, "genres")
date_classifier = KNNCreator(date_dataset, "release_date")
classifiers = [age_classifier, length_classifier, genre_classifier, date_classifier] #For simplicity
#Run the classifier.
for classifier in classifiers:
    classifier.classifier_init() #Start the classifier (Setting up the data by splitting it into training and testing).
    classifier.generate_confusion_matrix() #Generate confusion matrix for a visual representation of the accuracy of the model.
    classifier.train_kfold() #Train the model using KFOLD.
    classifier.save_model() #Save the model using pickle.