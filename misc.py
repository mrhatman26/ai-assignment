import tkinter as t
import random as r
import sys, os, platform, traceback
from tkinter import filedialog as f
from tkinter import messagebox

def pause():
    input("(Press ENTER to continue)")

def str_to_int_test(text):
    if type(text) == str:
        try:
            return True
        except:
            return False
    elif type(text) == int:
        return True
    else:
        return False

def get_valid_number(message):
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
    return len(item) - 1

def print_random_list(list_var):
    if type(list_var) == list:
        if len(list_var) > 0:
            print(list_var[r.randint(0, len(list_var) - 1)])
        else:
            print("ERROR [print_random_list]: Given list is empty.")
    else:
        print("ERROR [print_random_list]: Given list is NOT a list!")

def load_file():
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

def save_file(data):
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

def ask_question(title, message):
    window = t.Tk()
    window.withdraw()
    answer = messagebox.askyesno(title, message)
    window.destroy()
    return answer

def show_error(title, message):
    window = t.Tk()
    window.withdraw()
    messagebox.showerror(title, message)
    window.destroy()

def show_message(title, message):
    window = t.Tk()
    window.withdraw()
    messagebox.showinfo(title, message)
    window.destroy()

def show_warning(title, message):
    window = t.Tk()
    window.withdraw()
    messagebox.showwarning(title, message)
    window.destroy()

def get_os_clear():
    my_os = platform.system()
    clear = None
    if my_os == "Darwin" or my_os == "Linux":
        clear = lambda: os.system('clear')
    else:
        clear = lambda: os.system('cls')
    return clear

def error_exit(exception):
    print("Failed.\nError: " + str(exception))
    print(str(traceback.format_exc()))
    pause()
    sys.exit()