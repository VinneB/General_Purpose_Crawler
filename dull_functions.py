#This file holds boring functions that perform neccessary functins like deleting and writing files
from urllib.parse import urlparse
import os
import os.path
import shutil

def write_file(file_path, data):
    with open(file_path, "w") as f:
        f.write(data)

def append_to_file(file_path, data):
    with open(file_path, 'a') as f:
        f.write(data)

def delete_file_contents(file_path):
    with open(file_path, 'w') as f:
        f.write('')

def file_to_set(file_path):
    foobar = set()
    with open(file_path, 'r') as f:
        for line in f:
            foobar.add(line)
    return foobar

def container_to_file(container, file_path):
    delete_file_contents(file_path)
    for object in container:
        append_to_file(file_path, object)

def create_dir(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)
    else:
        print("Error: {} directory already exists".format(dir))
        override = input("Would you like to overwrite[YES/NO]?: ").upper()
        if override == "YES":
            delete_dir(dir)
            os.makedirs(dir)
        else:
            print("create_dir aborted")
            return None

def delete_dir(dir):
    if os.path.isdir(dir):
        shutil.rmtree(dir)
    else:
        print("Directory doesn't exist")
        return None
        
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        print("Error: URL not parsed")
        return ''


def get_domain_name(url):
    try:
        subdomain = get_sub_domain_name(url)
        subdomain = subdomain.split(".")
        return subdomain[-2] + "." + subdomain[-1]
    except:
        return ''

def remove_duplicates(item_list):
    l = list(dict.fromkeys(item_list))
    return l