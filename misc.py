import tkinter as t
import random as r
import sys, os, platform, traceback
from tkinter import filedialog as f
from tkinter import messagebox

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

def get_valid_number(message): #Remove
    no = 0
    while True:
        try:
            no = int(input(message))
            break
        except:
            print("Please enter a valid number!")
            input("(Press ENTER to continue)")
            print()
    return no

def zlen(item):
    #Returns the length of a list, but reduces it by one.
    return len(item) - 1

def print_random_list(list_var): #Remove
    if type(list_var) == list:
        if len(list_var) > 0:
            print(list_var[r.randint(0, len(list_var) - 1)])
        else:
            print("ERROR [print_random_list]: Given list is empty.")
    else:
        print("ERROR [print_random_list]: Given list is NOT a list!")

def load_file(): #Remove
    window = t.Tk()
    window.withdraw()
    file = t.filedialog.askopenfile(mode="r", filetypes=[("Text File", "*.txt")])
    window.destroy()
    if file is None:
        print("No file selected")
        return None
    else:
        print("File selected: " + str(file.name))
        return file

def save_file(data): #Remove
    window = t.Tk()
    window.withdraw()
    save_file = t.filedialog.asksaveasfile(filetypes=[("Text File", "*.txt")], defaultextension='*.txt')
    if save_file is None:
        print("File save has been cancelled")
        return False
    if type(data) == list:
        for line in data:
            if type(line) == list:
                for letter in line:
                    save_file.write(letter)
            else:
                save_file.write(line)
            save_file.write("\n")
    else:
        save_file.write(str(data))
    print("Data saved to: " + save_file.name)
    save_file.close()
    window.destroy()
    return True

def ask_question(title, message): #Remove
    window = t.Tk()
    window.withdraw()
    answer = messagebox.askyesno(title, message)
    window.destroy()
    return answer

def show_error(title, message): #Remove
    window = t.Tk()
    window.withdraw()
    messagebox.showerror(title, message)
    window.destroy()

def show_message(title, message): #Remove
    window = t.Tk()
    window.withdraw()
    messagebox.showinfo(title, message)
    window.destroy()

def show_warning(title, message): #Remove
    window = t.Tk()
    window.withdraw()
    messagebox.showwarning(title, message)
    window.destroy()

def get_os_clear():
    #Detects the OS being used and returns the clear screen command for that OS.
    my_os = platform.system()
    clear = None
    if my_os == "Darwin" or my_os == "Linux":
        clear = lambda: os.system('clear')
    else:
        clear = lambda: os.system('cls')
    return clear

def error_exit(exception):
    #Prints the given exception then forces the program to exit to avoid more errors.
    print("Failed.\nError: " + str(exception))
    print(str(traceback.format_exc()))
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