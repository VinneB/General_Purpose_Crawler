#This file contains high level procedures like creating project directories and their respective files as well as managing
#the threads, settings, type, and specifications of crawls
from dull_functions import *
from spider import Spider
import os
import os.path
import threading
from queue import Queue
from time import sleep

SAVE_TIME = 30
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
                write_file(crawl_dir + get_domain_name(url) + "\\domain_websites.txt", '')
        else:
            for url in urls:
                create_dir(crawl_dir + url)
        return crawl_dir

    def text_crawl(self, urls, num_of_threads, specified_text, domain_search=False):
        crawl_dir = self.create_crawl_dir(urls, domain_search)
        #Calls domain search to return a list of all webpages in the domain of the specified webpages.
        if domain_search == True:
            self.domain_search(urls, num_of_threads, crawl_dir)


    def link_crawl(self, urls, num_of_threads):
        pass

    def custom_crawl(self, urls, num_of_threads, tags, attrs, domain_search):
        pass

    def domain_search(self, urls, num_of_threads, crawl_dir):
        crawled_domains = list()
        save_lock = True
        
        def save():
            """Functions which saves crawled data to save_file at an interval of 'SAVE_TIME' seconds"""
            while True:
                sleep(SAVE_TIME)
                if not save_lock:
                    break
                temp_container = list(crawled)
                container_to_file(temp_container, save_file)
                print("Crawl data saved to {}".format(save_file))

        def crawl():
            while True:
                if not lock:
                    break
                site = queue.get()
                links = Spider.return_domain_links(site)
                crawl_queue.extend(links)
                


        for url in urls:
            #For the domain of each website(if two websites share a domain it will only crawl once), it will place all the
            #crawled websites into 'crawled' which regurally gets saved into 'domain_websites.txt' inside the domain folder
            #NECESSARY VARS
            lock = True
            domain_name = get_domain_name(url)
            #Ensures each domain is only crawled twice
            if domain_name in crawled_domains:
                continue
            crawled = list()
            crawl_queue = list()
            queue = Queue()
            save_file = crawl_dir + domain_name + "\\domain_websites.txt"
            #Gathers links in url using Spider init function and adds them to crawl queue
            initial_spider = Spider(url)
            crawl_queue.extend(initial_spider.base_page_links)
            #Create threads
            save_t = threading.Thread(target=save, daemon=True)
            save_t.start()
            for _ in num_of_threads:
                t = threading.Thread(target=crawl, daemon=True)
                t.start()
                print("{} initialized.".format(threading.current_thread().name))

            while len(crawl_queue) > 0:
                for url in crawl_queue:
                    queue.put(url)
                queue.join()

            lock = False
            container_to_file(crawled, save_file)

        save_lock = False


    @staticmethod
    def load_project(path):
        pass
        
        