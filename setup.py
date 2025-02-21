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

def clean_remove_other_columns(dataset, save_column):
    columns_to_remove = ["movie_rated", "run_length", "genres", "release_date"]
    try:
        print("Dropping columns from other datasets...", end="")
        columns_to_remove.pop(columns_to_remove.index(save_column))
        dataset = dataset.drop(columns_to_remove, axis=1)
        print("Done.")
    except Exception as e:
        error_exit(e)
    return dataset

def clean_normalise_boolean(dataset, column_name, split_type=None):
    print("\n**Normalising " + str(column_name) + " column**")
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
    #After this, save the dataset.
    try:
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Normalise " + column_name + ").csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset

def clean_normalise_months(dataset):
    print("\n**Normalising release_date column**")
    #The months of the year are known already, so to avoid an unnecessary loop, they are defined in this list for the purpose of indexing.
    months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
    try:
        print("Converting release_date values to numbers...", end="")
        y = 0
        for rows in dataset["release_date"]:
            values = rows.lower().split(" ") #Split the row into a list
            for month in months:
                #If one of the values of this list are in the months list, that means it represents the month.
                if month in values:
                    index = values.index(month)
                    #So get the index of that month in the split row list.
                    dataset.loc[y, "release_date"] = months.index(values[index]) #And use that index to get the index of the row month from the list of months.
                    #Sorry if that is confusing, I'm not sure how to better describe it.
            y += 1
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        #After this, save the dataset.
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Normalise months).csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset

def clean_normalise_runtime(dataset):
    print("\n**Normalising run_length column**")
    try:
        print("Converting run_length from hours and minutes to minutes...", end="\n")
        y = 0
        for row in dataset["run_length"]:
            print(row)
            row = row.split(" ")
            hours = 0
            minutes = 0
            #Get minutes and seonds from the row. Annoyingly, these values contain the strings "h" and "min" which need to be replaced.
            #Also, some movies have their runtime as hours only, no minutes.
            if len(row) == 1:
                if "h" in row[0]:
                    hours = row[0].replace("h", "")
                else:
                    minutes = row[0].replace("min", "")
            else:
                if "h" in row[0]:
                    hours = row[0].replace("h", "")
                    minutes = row[1].replace("min", "")
                else:
                    minutes = row[0].replace("min", "")
                    hours = row[1].replace("h", "")
            #Check hours and minutes can be converted to integers. Raise exception if they cannot.
            if str_to_int_test(hours) is True:
                hours = int(hours)
            else:
                raise Exception("Cannot normalise movie hours as they are a string (not a int) equal to '" + str(hours) + "' that is of type " + str(type(hours)))
            if str_to_int_test(minutes) is True:
                minutes = int(minutes)
            else:
                raise Exception("Cannot normalise movie minutes as they are a string (not an int) equal to '" + str(minutes) + "' that is of type " + str(type(hours)))
            #Convert movie time to minutes only by adding 60 minutes for each hour.
            while hours > 0:
                minutes += 60
                hours -= 1
            #Save the minutes to the current row.
            dataset.loc[y, "run_length"] = minutes
            y += 1
        print("Done.")
    except Exception as e:
        error_exit(e)
    try:
        #After this, save the dataset.
        print("Saving modified dataset...", end="")
        dataset.to_csv("./saved_data/Movie Dataset (Normalise runtime).csv", sep=",")
        print("Done.")
    except Exception as e:
        print("Failed.")
    return dataset