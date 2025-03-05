import sys, os, platform, traceback, shutil, ast
import pandas as pd
from file_paths import *

def pause(exit=False): #Stops the program from running by requestiong input. Anything inputted is not used.
    if exit is False:
        input("(Press ENTER to Continue)")
    else:
        input("(Press ENTER to Exit)")

def str_to_int_test(text):
    #Checks if a string can be converted to an integer.
    #If the string can be converted, it returns True.
    #If value is ALREADY an integer, it returns True.
    #If the string cannot be converted, it returns False.
    #If the value is NOT a string or an integer, it returns False.
    if type(text) == str:
        try:
            return True
        except:
            return False
    elif type(text) == int:
        return True
    else:
        return False

def zlen(item):
    #Returns the length of a list, but reduces it by one.
    return len(item) - 1

def get_os_clear():
    #Detects the OS being used and returns the clear screen command for that OS.
    my_os = platform.system()
    clear = None
    if my_os == "Darwin" or my_os == "Linux":
        clear = lambda: os.system('clear')
    else:
        clear = lambda: os.system('cls')
    return clear

def error_exit(exception, skip=False):
    #Prints the given exception then forces the program to exit to avoid more errors.
    print("Failed.\nError: " + str(exception))
    print(str(traceback.format_exc()))
    if skip is False:
        pause(True)
        sys.exit()

def create_ditto_list(length, value_to_repeat):
    #Creates a list that is the requested length and makes every value of that list
    #the same as vale_to_repeat. Used in this program to create a list that is entirely False
    #with values being changed to True based off of the data.
    new_list = []
    index = 0
    while index < length:
        new_list.append(value_to_repeat)
        index += 1
    return new_list

def check_save_dir_exists():
    #Makes sure ./saved_data/ and ./saved_data/models/ directories exist.
    #If they don't they are created.
    if os.path.exists(saved_data_dir) is not True:
        os.makedirs(saved_data_dir)
    if os.path.exists(saved_models_dir) is not True:
        os.makedirs(saved_models_dir)
    if os.path.exists(saved_models_knn_dir) is not True:
        os.makedirs(saved_models_knn_dir)
    if os.path.exists(saved_models_linear_dir) is not True:
        os.makedirs(saved_models_linear_dir)
    if os.path.exists(saved_graphs_dir) is not True:
        os.makedirs(saved_graphs_dir)
    if os.path.exists(saved_maps_dir) is not True:
        os.makedirs(saved_maps_dir)

def check_and_move_models_knn():
    try:
        print("Moving KNN models to static...", end="")
        #Check KNN models exist and copy them to static
        if os.path.exists(saved_models_dir) is True:
            if os.path.exists(saved_models_knn_dir) is True:
                if len(os.listdir(saved_models_knn_dir)) > 0:
                    if len(os.listdir(saved_models_knn_dir)) == 4:
                        if os.path.exists(static_models_dir) is False:
                            os.makedirs(static_models_dir)
                        if os.path.exists(static_models_knn_dir) is False:
                            os.makedirs(static_models_knn_dir)
                        shutil.rmtree(static_models_knn_dir)
                        shutil.copytree(saved_models_knn_dir, static_models_knn_dir)
                    else:
                        raise Exception("KNN directory does not have enough models. Expected 4 models got " + str(len(os.listdir(saved_models_knn_dir))))
                else:
                    raise Exception("KNN directory has no models.")
            else:
                raise Exception("KNN directory does not exist in models directory.")
        else:
            raise Exception("Models directory does not exist.")
    except Exception as e:
        error_exit(e)
    print("Done.")

def check_and_move_models_linear():
    try:
        print("Moving linear models to static...", end="")
        #Check KNN models exist and copy them to static
        if os.path.exists(saved_models_dir) is True:
            if os.path.exists(saved_models_linear_dir) is True:
                if len(os.listdir(saved_models_linear_dir)) > 0:
                    if len(os.listdir(saved_models_linear_dir)) == 4:
                        if os.path.exists(static_models_dir) is False:
                            os.makedirs(static_models_dir)
                        if os.path.exists(static_models_linear_dir) is False:
                            os.makedirs(static_models_linear_dir)
                        shutil.rmtree(static_models_linear_dir)
                        shutil.copytree(saved_models_linear_dir, static_models_linear_dir)
                    else:
                        raise Exception("KNN directory does not have enough models. Expected 4 models got " + str(len(os.listdir(saved_models_linear_dir))))
                else:
                    raise Exception("KNN directory has no models.")
            else:
                raise Exception("KNN directory does not exist in models directory.")
        else:
            raise Exception("Models directory does not exist.")
    except Exception as e:
        error_exit(e)
    print("Done.")

def check_and_move_maps():
    try:
        print("Moving maps to static...", end="")
        #Check maps exist and copy them to static
        if os.path.exists(saved_maps_dir):
            if len(os.listdir(saved_maps_dir)) > 0:
                if os.path.exists(static_maps_dir) is False:
                    os.makedirs(static_maps_dir)
                shutil.rmtree(static_maps_dir)
                shutil.copytree(saved_maps_dir, static_maps_dir)
            else:
                raise Exception("Maps directory is empty.")
        else:
            raise Exception("Maps directory does not exist.")
    except Exception as e:
        error_exit(e)
    print("Done.")

def ask_question(message):
    #Asks the user a question and loops until the enter "Yes", "Y", "No" or "N".
    #The user entering "Yes" or "Y" will return True.
    #The user entering "No" or "N" will return False.
    while True:
        print(message)
        answer = input("Yes/No (Y/N): ").upper()
        if answer in "YES" "Y":
            return True
        elif answer in "NO" "N":
            return False
        else:
            print("Please enter Yes (Y) or No (N)")
            pause()
            print("\n")

def load_dataset_map(dataset_name, is_bool=False, is_static=False):
    #Loads a dataset map from either the static directory or the saved_data directory.
    #If is_bool is True, the boolean map will be loaded instead.
    #If the map file is found, it is read and converted to a list which is then returned.
    #If the map files is not found, None is returned instead.
    try:
        if is_bool is False:
            if is_static is False:
                map_path = saved_maps_dir + dataset_name + "_unique_vals.txt"
            else:
                map_path = static_maps_dir + dataset_name + "_unique_vals.txt"
        else:
            if is_static is False:
                map_path = saved_maps_dir + dataset_name + "_unique_vals_int_to_bool.txt"
            else:
                map_path = static_maps_dir + dataset_name + "_unique_vals_int_to_bool.txt"
        print("Opening " + map_path)
        map_file = open(map_path, "r")
        map_list = []
        for unique_val in map_file:
            unique_val = unique_val.replace("\n", "")
            if unique_val != "":
                map_list.append(unique_val)
        map_file.close()
        return map_list
    except Exception as e:
        return None
    
def get_model_path(dataset_name, model="knn", is_static=False):
    #Gets the path of the dataset's model from either the static directory or the saved_data directory.
    #If the model is KNN, it gets the KNN model, else it gets the linear regression model instead.
    try:
        print("Getting model path...", end="")
        if is_static is False:
            if model == "knn":
                model_path = saved_models_knn_dir + dataset_name + "_model"
            else:
                model_path = saved_models_linear_dir + dataset_name + "_model"
        else:
            if model == "knn":
                model_path = static_models_knn_dir + dataset_name + "_model"
            else:
                model_path = static_models_linear_dir + dataset_name + "_model"
        print("Done.\nPath is " + model_path)
        return model_path
    except Exception as e:
        error_exit(e, skip=True)
        return None
    
def check_list_bool(list_val):
    #Checks a list to make sure all of it's values are boolean.
    #Returns True if they all are or False if they aren't.
    is_bool = True
    for item in list_val:
        try:
            bool(item)
        except:
            is_bool = False
            break
    return is_bool
    
def str_to_list(str_val): #Becase ast literal_eval doesn't damn well work.
    #Converts an string representation of a list into a list.
    str_val = str_val.replace("[", "").replace("]", "")
    str_val = str_val.split(", ")
    return str_val

def confusion_to_dataset(confusion_matrix):
    #Converts a confusion matrix into a pandas dataframe.
    return pd.DataFrame(confusion_matrix, index=range(0, len(confusion_matrix)), columns=range(0, len(confusion_matrix)))

def input_to_map(actual_data, map_data, is_bool=False):
    #Converts the actual data into a mapped value:
    #If is_bool is false, the index of actual_data as it appears in map data is returned.
    #Else, actual data is converted into a binary list to represent the mapped values and the binary list is returned.
    if is_bool is False:
        return map_data.index(actual_data)
    else:
        map_list = create_ditto_list(len(map_data), 0)
        for item in actual_data:
            item = item.lower()
            if item in map_data:
                map_list[map_data.index(item)] = 1
        return map_list
    
def get_closest_map(actual_data, map_data):
    #Attempts to find the most similar mapped value to the entered data.
    #This is only used for linear regression.
    print("Converting map list strings to lists...", end="")
    for i in range(0, len(map_data)):
        map_data[i] = map_data[i].replace("[", "").replace("]", "")
        map_data[i] = map_data[i].split(", ")
        for t in range(0, len(map_data[i])):
            map_data[i][t] = int(map_data[i][t])
    print("Done.\nGetting closest map from entered data...", end="")
    if len(actual_data) == len(map_data[0]):
        counter_list = create_ditto_list(len(map_data), 0)
        index = 0
        for item in map_data:
            for i in range(0, len(map_data[index])):
                if actual_data[i] == item[i]:
                    counter_list[index] += 1
            index += 1
        print("Done.\nFinding index with highest match...", end="")
        highest_index = 0
        highest_number = 0
        index = 0
        for item in counter_list:
            if item > highest_number:
                highest_index = index
                highest_number = item
            index += 1
        print("Done.")
        return highest_index
    else:
        print("Failed.")
        raise Exception("Actual Data is not the same length as map data.")