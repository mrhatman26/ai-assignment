import pandas as pd
import sys
from setup import *
from misc import *
pd.options.mode.chained_assignment = None 
pd.set_option('display.max_columns', None) #Allows for ALL columns to be printed.
pd.set_option('display.max_rows', None) #Allows for ALL rows to be printed.
#Load CSV file using Pandas.
print("Loading dataset...", end="")
try:
    movie_dataset = pd.read_csv("IMDb Movies Dataset.csv")
except Exception as e:
    error_exit(e)
print("Done")
show_dataset(movie_dataset)
movie_dataset = clean_remove_unused(movie_dataset)
movie_dataset = clean_normalise_boolean(movie_dataset, "genres", "; ")
