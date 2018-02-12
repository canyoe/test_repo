import os


def run1():

    print("In module dirlist")
    files = os.listdir(".")
    print(files)
    return str(files)

