import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split #Importing of the required modules from sklearn to allow for the training of the A.I.
from sklearn.linear_model import LinearRegression
from misc import * 

class LinearCreator():
    dataset = None
    dataset_name = ""
    x, y, x_train, y_train, x_test, y_test = None, None, None, None, None, None
    def __init__(self, dataset, dataset_name):
        try:
            print("Setting up Linear Regression model for " + dataset_name + ".")
            self.dataset = dataset
            self.dataset_name = dataset_name
            print("Creating X and Y of model...", end="")
            self.x = self.dataset[self.dataset_name].drop(columns="rating")
            self.y = self.dataset["rating"].drop(columns=self.dataset_name)
            print("Creating test and training data...", end="")
            print("Done.")
            self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, random_state=11, test_size=0.30)
            print("Done.")
            print(dataset_name + " x_train shape is " + str(self.x_train.shape) + "\ny_train shape is " + str(self.y_train.shape))
            print(dataset_name + " x_test shape is " + str(self.x_test.shape) + "\ny_test shape is " + str(self.y_test.shape))
            pause()
        except Exception as e:
            error_exit(e)