import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split #Importing of the required modules from sklearn to allow for the training of the A.I.
#test_train_split splits the data between training data and test data/
from sklearn.neighbors import KNeighborsClassifier #KNN is what I've used to train the A.I
from sklearn.metrics import confusion_matrix #Allows for the creation of a confusion matrix
from sklearn.metrics import classification_report #Allows for the creation of classification report
from sklearn.model_selection import KFold #Allows for KFold validation
from sklearn.model_selection import cross_val_score #Allows for evaluation of a score by cross validation
from misc import *

class KNNCreator():
    dataset = None
    dataset_name = ""
    dataset_map = {}
    classifier = None
    predicted = None
    expected = None
    wrong = None
    confusion = None
    class_report = None
    kfold = None
    kfold_scores = None
    x, y, x_train, y_train, x_test, y_test = None, None, None, None, None, None
    def __init__(self, dataset, dataset_name):
        try:
            print("Setting up KNN model for " + dataset_name + ".")
            self.dataset = dataset
            self.dataset_name = dataset_name
            #First, create a map of the dataset from the text file generated in setup.py ("column_unique_vals.txt.txt"). 
            #If the file exists, then it doesn't need a map.
            try:
                index = 0
                for line in open("./saved_data/" + dataset_name + "_unique_vals.txt", "r"):
                    self.dataset_map[line.replace("\n", "")] = index
                    index += 1
                print("Done.")
            except:
                self.dataset_map = None
            if self.dataset_map is not None:
                print("Mapping for " + self.dataset_name + " is:\n")
                for key, value in self.dataset_map.items():
                    print(str(key) + ": " + str(value))
            print("\n")
            #Setting the selected column as X as in the x axis of a graph.
            #movie_rated is dropped otherwise it'd also be apart of the X axis which wouldn't make sense.
            self.x = dataset[self.dataset_name].drop(columns="rating")
            #Ditto, but movie rated is set to the Y axis and the selected column is dropped instead.
            self.y = dataset["rating"].drop(columns=self.dataset_name)
            #Setting up the training data. Here, 30% of the data becomes training data while the rest is test data.
            #Training data is like putting a label on a banana saying that it is a banana and then telling someone, "This is a banana".
            #Test data meanwhile, does not have that label. It's like asking someone, "what is this yellow object?" and hoping they say "banana".
            if type(self.x[0]) != list:
                print("Data is not a list, converting it to a list...", end="")
                for i in range(0, len(self.x)):
                    self.x[i] = [self.x[i]]
                print("Done.")
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=11, test_size=0.30)
            #Converting the training and test data to numpy arrays that are integers.
            self.x_train = np.array(list(self.x_train), dtype=int)
            self.x_test = np.array(list(self.x_test), dtype=int)
            self.y_train = np.array(list(self.y_train), dtype=int)
            self.y_test = np.array(list(self.y_test), dtype=int)
            print("Done.")
            print(dataset_name + " x_train shape is " + str(self.x_train.shape) + "\ny_train shape is " + str(self.y_train.shape))
            print(dataset_name + " x_test shape is " + str(self.x_test.shape) + "\ny_test shape is " + str(self.y_test.shape))
        except Exception as e:
            error_exit(e)
        if type(self.dataset[self.dataset_name][0]) == list:
            self.confirm_length()

    def confirm_length(self):
        try:
            print("Confirming all data of " + self.dataset_name + " is the same length...", end="")
            unique_length = 0
            for item in self.dataset[self.dataset_name]:
                if unique_length == 0:
                    unique_length = len(item)
                else:
                    if len(item) != unique_length:
                        raise Exception(self.dataset_name + " dataset does not have equal list lengths.")
            print("Done.")
        except Exception as e:
            error_exit(e)

    def classifier_init(self):
        try:
            print("Initiating KNN classifier...", end="")
            self.classifier = KNeighborsClassifier()
            print("Done.\nFitting training data...", end="")
            self.classifier.fit(X=self.x_train, y=self.y_train)
            print("Done.\nTesting model with test data...", end="")
            self.predicted = self.classifier.predict(X=self.x_test)
            self.expected = self.y_test
            print("Done.")
            print("Predicted is " + str(self.predicted) + "\nExpected is " + str(self.expected))
            self.wrong = [(p, e) for (p, e) in zip(self.predicted, self.expected) if p != e]
            print("KNN score is ", f'{self.classifier.score(self.x_test, self.y_test):.2%}')
            print("")
        except Exception as e:
            error_exit(e)

    def generate_confusion_matrix(self):
        try:
            print("Creating confusion matrix...", end="")
            self.confusion = confusion_matrix(y_true=self.expected, y_pred=self.predicted)
            print("Done.\nConfusion matrix is:\n" + str(self.confusion) + "\nGenerating classification report...", end="")
            self.class_report = classification_report(self.expected, self.predicted)
            print("Done.\nClassification report is:\n" + str(self.class_report))
            print("")
        except Exception as e:
            error_exit(e)

    def train_kfold(self):
        try:
            print("Training " + self.dataset_name + " model using KFOLD...", end="")
            self.kfold = KFold(n_splits=len(self.dataset[self.dataset_name]) - 1, random_state=11, shuffle=True)
            self.kfold_scores = cross_val_score(self.classifier, X=np.array(list(self.dataset[self.dataset_name]), dtype=int), y=np.array(list(self.dataset["rating"]), dtype=int), cv=self.kfold)
            print("Done.")
            print("")
        except Exception as e:
            error_exit(e)

    def save_model(self):
        try:
            print("Saving " + self.dataset_name + " model using pickle...", end="")
        except Exception as e:
            error_exit(e)