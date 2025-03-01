import sys, os, platform, traceback
import pandas as pd

def pause(): #Stops the program from running by requestiong input. Anything inputted is not used.
    input("(Press ENTER to continue)")

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
        pause()
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
    if os.path.exists("./saved_data/") is not True:
        os.makedirs("./saved_data/")
    if os.path.exists("./saved_data/models/") is not True:
        os.makedirs("./saved_data/models/")
    if os.path.exists("./saved_data/models/knn/") is not True:
        os.makedirs("./saved_data/models/knn/")
    if os.path.exists("./saved_data/models/linear/") is not True:
        os.makedirs("./saved_data/models/linear/")
    if os.path.exists("./saved_data/graphs/") is not True:
        os.makedirs("./saved_data/graphs/")
    if os.path.exists("./saved_data/maps/") is not True:
        os.makedirs("./saved_data/maps/")

def ask_question(message):
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

def load_dataset_map(dataset_name, is_bool=False):
    try:
        if is_bool is False:
            map_path = "./saved_data/maps/" + dataset_name + "_unique_vals.txt"
        else:
            map_path = "./saved_data/maps/" + dataset_name + "_unique_vals_int_to_bool.txt"
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
    
def check_list_bool(list_val):
    is_bool = True
    for item in list_val:
        try:
            bool(item)
        except:
            is_bool = False
            break
    return is_bool
    
def str_to_list(str_val): #Becase ast literal_eval doesn't damn well work.
    str_val = str_val.replace("[", "").replace("]", "")
    str_val = str_val.split(", ")
    return str_val

def confusion_to_dataset(confusion_matrix):
    return pd.DataFrame(confusion_matrix, index=range(0, len(confusion_matrix)), columns=range(0, len(confusion_matrix)))