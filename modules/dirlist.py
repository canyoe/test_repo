import os

def run(**args):

    print("In module dirlist")
    files = os.listdir(".")

    return str(files)

