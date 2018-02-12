import os


def run(*args, **kwargs):

    print("In module dirlist")
    files = os.listdir(".")
    #print(files)
    return str(files)

