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
            pass
        except Exception as e:
            error_exit(e)