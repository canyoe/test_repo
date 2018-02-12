import os


print("DIRLIST WAS IMPORTED")
def run():

    print("In module dirlist")
    files = os.listdir(".")

    return str(files)

