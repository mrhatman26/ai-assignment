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
    #Finally, save the modified dataset
    try:
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Remove Unused Columns).csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset

def clean_normalise_boolean(dataset, column_name, split_type=None): #Modify this to work for release date as well.
    print("**Normalising " + str(column_name) + " column**")
    #Loop 1
    try:
        #First get all unique values of the specified column.
        unique_vals = []
        print("Getting unique values of column...", end="")
        for row in dataset[column_name]:
            if split_type is not None:
                for value in row.split(split_type):
                    value = value.lower()
                    if value not in unique_vals and value != "" and value != " ":
                        unique_vals.append(value.lower())
            else:
                row = row.lower()
                if row not in unique_vals and row != "" and row != " ":
                    unique_vals.append(row.lower())
        print("Done.\nUnique values detected are:")
        for item in unique_vals:
            print("'" + item + "'")
    except Exception as e:
        error_exit(e)
    #Loop 2
    #Consider doing this stage in loop 1?
    try:
        #Then, create new columns from those unique values.
        print("Adding new columns for each unique value...", end="")
        for value in unique_vals:
            if value != "" and value != " ":
                dataset[column_name + "_" + str(value)] = False
        print("Done.")
    except Exception as e:
        error_exit(e)
    #Loop 3
    try:
        #Then, if a row has that unique value, set its corresponding column to True.
        #E.G: If a movie has an age rating of PG, set that row's PG column to True.
        print("Setting unique columns to True based off of original column values...", end="")
        y = 0
        for rows in dataset[column_name]:
            if split_type is not None:
                for value in rows.split(split_type):
                    if value != "" and value != " ":
                        dataset.loc[y, column_name + "_" + str(value).lower()] = True
            else:
                dataset.loc[y, column_name + "_" + str(row).lower()] = True
            y += 1
        print("Done.")
    except Exception as e:
        error_exit(e)
    #Loop 4
    try:
        #Then make sure at least one of the created columns is True for each row.
        print("Checking all rows have at least one of the new columns set to True...", end="")
        for index, row in dataset.iterrows():
            col_no = 0
            has_value = False
            for column in row:
                if column_name + "_" in dataset.columns[col_no]:
                    if column == True:
                        has_value = True
                col_no += 1
            if has_value is False:
                raise Exception("One or more rows have no True values when normalising column " + column_name)
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        #Finally, remove the specified column as it will no longer be needed.
        print("Removing " + column_name + " column...", end="")
        dataset = dataset.drop([column_name], axis=1)
        print("Done.")
    except Exception as e:
        error_exit(e)
    #After this, ask the user if they would like the normalised dataset to be saved.
    try:
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Normalise " + column_name + ").csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset

def clean_normalise_months(dataset):
    print("**Normalising release_date column**")
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    try:
        print("Converting release_date values to numbers...", end="")
        y = 0
        for rows in dataset["release_date"]:
            values = rows.lower().split(" ")
            for month in months:
                if month in values:
                    index = values.index(month)
                    dataset.loc[y, "release_date"] = months.index(values[index])
            y += 1
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Normalise months).csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset