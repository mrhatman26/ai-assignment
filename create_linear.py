import numpy as np
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split #Importing of the required modules from sklearn to allow for the training of the A.I.
from sklearn.linear_model import LinearRegression
from misc import * 

class LinearCreator():
    dataset = None
    dataset_name = ""
    x, y, x_train, y_train, x_test, y_test = None, None, None, None, None, None
    linear = None
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
        except Exception as e:
            error_exit(e)