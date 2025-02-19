import pandas as pd
from misc import *

def clean_remove_unused(dataset):
    print("**Cleaning data**")
    print("Dropping num_* columns...", end="")
    try:
        dataset = dataset.drop(["name", "year", "num_raters", "num_reviews"], axis=1)
        #Dropping the name, year, num_raters and num_reviews columns as these will not be used to create the models.
    except Exception as e:
        error_exit(e)
    print("Done.")
    print("Dropping rows with blanks...", end="")
    try:
        dataset = dataset[~dataset.isin(['[]']).any(axis=1)]
    except Exception as e:
        error_exit(e)
    print("Done.")
    if ask_question("Save Dataset?", "Would you like to save the dataset as it currently is to a file?") is True:
        dataset.to_csv("Movie Dataset (Edit 1).csv", sep=",")
    return dataset

def clean_normalise(dataset):
    pd.options.mode.chained_assignment = None 
    print("**Normalising genres column**")
    try:
        #First get all the unique genres.
        unique_genres = []
        print("Getting unique genres...", end="")
        for genres in dataset["genres"]:
            for genre in genres.split("; "):
                genre = genre.lower()
                if genre not in unique_genres and genre != "" and genre != " ":
                    unique_genres.append(genre)
        print("Done.\nDetected genres are:")
        for item in unique_genres:
            print("'" + item + "'")
        pause()
    except Exception as e:
        error_exit(e)
    try:
        print("Adding new columns for each unique genre...", end="")
        for genre in unique_genres:
            genre = str(genre).lower()
            if genre != "" and genre != " ":
                dataset["genre_" + str(genre)] = False #Create a new column for each genre on each row and set it to equal
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        print("Setting genre columns to True based off of genres column..." , end="")
        y = 0
        for genres in dataset["genres"]:
            for genre in genres.split("; "):
                if genre != "" and genre != " ":
                    dataset.loc[y, "genre_" + str(genre).lower()] = True
            y += 1
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        print("Checking all rows have at least ONE genre...", end="")
        for index, row in dataset.iterrows():
            col_no = 0
            has_genre = False
            for column in row:
                if "genre_" in dataset.columns[col_no]:
                    if column == True:
                        has_genre = True
                col_no += 1
            if has_genre is False:
                raise Exception("One or more rows of the dataset have no genres.")
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        print("Removing genres column...", end="")
        dataset = dataset.drop(["genres"], axis=1)
        print("Done.")
    except Exception as e:
        error_exit(e)
    if ask_question("Save Dataset?", "Would you like to save the dataset as it currently is to a file?") is True:
        dataset.to_csv("Movie Dataset (Edit 2).csv", sep=",")
    show_dataset(dataset)