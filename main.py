#This file contains high level procedures like creating project directories and their respective files as well as managing
#the threads, settings, type, and specifications of crawls
from dull_functions import *
import spider
import os
import os.path
import threading
from queue import Queue
from time import sleep

ROOT_PROJECT_DIR = "C:\\Users\\VinneB\\Documents\\Web_Crawlers\\"
CONFIGS = ROOT_PROJECT_DIR + "configs.txt"
if not os.path.isdir(ROOT_PROJECT_DIR):
    create_dir(ROOT_PROJECT_DIR)
if not os.path.isfile(CONFIGS):
    write_file(CONFIGS, '')

current_project = None

#Importing of saved_configurations
class Config:
    configs = []

    def __init__(self, name, crawl_type, url_list, domain_search):
        self.name = name
        self.crawl_type = crawl_type
        self.urls = url_list
        self.domain_search = domain_search

    @staticmethod
    def import_configs(config_file):
        with open(config_file) as raw_config:
            raw_config.read()
        raw_config.split("\n")
        for configuration in raw_config:
            configuration.split(" ")
            Config.configs.append(Config(configuration[0], configuration[1], configuration[2], configuration[3]))

Config.import_configs(CONFIGS)

class Project:
    def __init__(self, project_name, crawl_num=0):
        print("Project ---- {}".format(project_name))
        #Stores Neccesary Vars
        self.project_name = project_name
        self.crawl_num = int(crawl_num)
        #Creating and formatting project directory
        print("Creating directory...")
            #Creates Directory
        self.project_dir = ROOT_PROJECT_DIR + project_name + "[GPC]\\"
        create_dir(self.project_dir)
            #Formats Properly
        write_file(self.project_dir + "project.txt" + "{}\n{}\n".format(self.project_name, self.crawl_num), '')

    def create_crawl_dir(self, urls, domain_search=False):
        crawl_dir = self.project_dir + "Crawl_{}\\".format(self.crawl_num)
        create_dir(crawl_dir)
        if domain_search == True:
            for url in urls:
                create_dir(crawl_dir + get_domain_name(url))
        else:
            for url in urls:
                create_dir(crawl_dir + url)
        return crawl_dir

    def text_crawl(self, urls, num_of_threads, specified_text, domain_search=False):
        crawl_dir = create_crawl_dir(urls, domain_search)
        #Calls domain search to return a list of all webpages in the domain of the specified webpages.
        if domain_search == True:
            self.domain_search(urls, num_of_threads, crawl_dir)


    def link_crawl(self, urls, num_of_threads):
        pass

    def custom_crawl(self, urls, num_of_threads, tags, attrs, domain_search):
        pass

    def domain_search(self, urls, num_of_threads, crawl_dir):
        crawled domains = list()
        def save(save_file, auto_time, queue):
            while True:
                sleep(auto_time)
                write_file

        for url in urls:
            #For the doimain of each website(if two websites share a domain it will only crawl once), it will place all the
            #
            domain_name = get_domain_name(url)
            crawled = list()
            crawl_queue           ]
            crawl_queue = Queue()


    @staticmethod
    def load_project(path):
        pass
        
        