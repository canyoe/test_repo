import os


def run1():

    print("In module dirlist")
    files = os.listdir(".")

    return str(files)

