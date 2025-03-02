import numpy as np
import pickle as pk
from file_paths import *
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split #Importing of the required modules from sklearn to allow for the training of the A.I.
from sklearn.linear_model import LinearRegression
from sklearn.metrics import confusion_matrix #Allows for the creation of a confusion matrix
from sklearn.metrics import classification_report #Allows for the creation of classification report
from sklearn.model_selection import KFold #Allows for KFold validation
from sklearn.model_selection import cross_val_score #Allows for evaluation of a score by cross validation
from misc import * 

class LinearCreator():
    dataset = None
    dataset_name = ""
    linear = None
    predicted = None
    expected = None
    confusion = None
    wrong = None
    class_report = None
    kfold = None
    kfold_scores = None
    x, y, x_train, y_train, x_test, y_test = None, None, None, None, None, None
    def __init__(self, dataset, dataset_name):
        try:
            print("Setting up Linear Regression model for " + dataset_name + ".")
            self.dataset = dataset
            self.dataset_name = dataset_name
            print("Creating X and Y of model...", end="")
            self.x = self.dataset[self.dataset_name].drop(columns="rating")
            self.y = self.dataset["rating"].drop(columns=self.dataset_name)
            print("Done.")
            if type(self.x[0]) != list:
                print("Data is not a list, converting it to a list...", end="")
                for i in range(0, len(self.x)):
                    self.x[i] = [self.x[i]]
                print("Done.")
            print("Creating test and training data...", end="")
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=11, test_size=0.30)
            self.x_train = np.array(list(self.x_train), dtype=int)
            self.x_test = np.array(list(self.x_test), dtype=int)
            self.y_train = np.array(list(self.y_train), dtype=int)
            self.y_test = np.array(list(self.y_test), dtype=int)
            print("Done.")
            print(dataset_name + " x_train shape is " + str(self.x_train.shape) + "\ny_train shape is " + str(self.y_train.shape))
            print(dataset_name + " x_test shape is " + str(self.x_test.shape) + "\ny_test shape is " + str(self.y_test.shape))
        except Exception as e:
            error_exit(e)

    def linear_init(self):
        try:
            print("Training " + self.dataset_name + " with Linear Regression...", end="")
            self.linear = LinearRegression()
            self.linear.fit(self.x_train, self.y_train)
            print("Done.\nScore is: " + str(self.linear.score(self.x_test, self.y_test)))
            self.predicted = self.linear.predict(self.x_test)
            self.expected = self.y_test
            print("Predicted is " + str(self.predicted) + "\nExpected is " + str(self.expected))
            self.wrong = [(p, e) for (p, e) in zip(self.predicted, self.expected) if p != e]
            self.predicted = np.array(list(self.predicted), dtype=int)
            print("KNN score is ", f'{self.linear.score(self.x_test, self.y_test):.2%}')
        except Exception as e:
            error_exit(e)

    def generate_confusion_matrix(self):
        #Generats a grid that is a visual representation of how accurate the model.
        try:
            print("Creating confusion matrix...", end="")
            self.confusion = confusion_matrix(y_true=self.expected, y_pred=self.predicted)
            print("Done.\nConfusion matrix is:\n" + str(self.confusion) + "\nGenerating classification report...", end="")
            self.class_report = classification_report(self.expected, self.predicted)
            print("Done.\nClassification report is:\n" + str(self.class_report))
            print("")
        except Exception as e:
            error_exit(e)

    def save_model(self):
        #Saves the generated model using the "pickle" library.
        #All models are saved to "./saved_data/models/knn/" for clarity.
        try:
            print("Saving " + self.dataset_name + " model using pickle...", end="")
            model_pickle_file = open(saved_models_linear_dir + self.dataset_name + "_model", "wb") #Open or create a file to save the model using pickle. "wb" is binary write mode.
            pk.dump(self.linear, model_pickle_file)
            model_pickle_file.close()
            print("Done.")
        except Exception as e:
            error_exit(e)