#This file contains high level procedures like creating project directories and their respective files as well as managing
#the threads, settings, type, and specifications of crawls
from dull_functions import *
from spider import Spider
import os
import os.path
import threading
from queue import Queue
from time import sleep

NUM_OF_THREADS = 8
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

#Config.import_configs(CONFIGS)

class Project:
    def __init__(self, project_name, crawl_num=0):
        print("Project ---- {}".format(project_name))
        #Stores Neccesary Vars
        self.project_name = project_name
        self.crawl_num = int(crawl_num)
        #Creating and formatting project directory
        print("Creating directory...")
        self.project_dir = ROOT_PROJECT_DIR + project_name + "[GPC]\\"
        create_dir(self.project_dir)
            #Formats Properly
        write_file(self.project_dir + "project.txt", "{}\n{}\n".format(self.project_name, self.crawl_num))

    def create_crawl_dir(self, urls, domain_search=False):
        crawl_dir = self.project_dir + "Crawl_{}\\".format(self.crawl_num)
        self.crawl_num +=1
        create_dir(crawl_dir)
        if domain_search == True:
            for url in urls:
                create_dir(crawl_dir + get_domain_name(url))
                write_file(crawl_dir + get_domain_name(url) + "\\domain_websites.txt", '')
        else:
            for url in urls:
                create_dir(crawl_dir + url)
        return crawl_dir


class Crawler:
    def __init__(self, project):
        """This is the crawler which you use to call crawl urls"""
        self.project = project

    def text_crawl(self, urls, specified_text, domain_search=False):
        if isinstance(urls, str):
            urls = [urls]
        crawl_dir = self.project.create_crawl_dir(urls, domain_search)
        save_file = [crawl_dir, None, "\\text_data.txt"]
        #Calls domain search to return a list of all webpages in the domain of the specified webpages.
        if domain_search:
            self.domain_search(urls, crawl_dir)
            urls = [get_domain_name(url) for url in urls]
        for url in urls:
            #NECESSARY VARS
            save_file[1] = url
            #Only exist if website has had it's domain searched
            domain_websites_file = crawl_dir + url + "\\domain_websites.txt"
            text_data_set = set()
            queue = Queue()
            kill_crawl_threads = False
            kill_save_threads = False
            if os.path.isfile(domain_websites_file):
                #Setup Threads
                thread_setup(thread_crawl, NUM_OF_THREADS, (Spider.return_specified_text, queue, text_data_set, None, kill_crawl_threads))
                thread_setup(thread_save, 1, (text_data_set, save_file, kill_save_threads))
                #Add urls from domain_websites to queue and begin crawling
                queue.put(file_to_set(domain_websites_file))
                queue.join()
                container_to_file(text_data_set, save_file)
            else:
                text_data_set = Spider.return_specified_text(url, specified_text)
                container_to_file(text_data_set, save_file)


    def link_crawl(self, urls):
        pass

    def custom_crawl(self, urls, tags, attrs, domain_search):
        pass

    @staticmethod
    def domain_search(base_urls, crawl_dir):
        """For the domain of each website(if two websites share a domain it will only crawl once), it will place all the
        crawled websites into 'crawled' which regurally gets saved into 'domain_websites.txt' inside the domain folder"""
        if isinstance(base_urls, str): base_urls = [base_urls]
        crawled_domains = list()
        first_url = True
        save_file = [crawl_dir, None, "\\domain_websites.txt"]
        
        for base_url in base_urls:
            #NECESSARY VARS
            domain_name = get_domain_name(base_url)
            #Ensures each domain is only crawled twice
            if domain_name in crawled_domains:
                continue
            crawled = set()
            crawl_queue = set([base_url])
            queue = Queue()
            #Updates the folder that the save thread is referencing
            save_file[1] = domain_name
            #Create threads
            if first_url:
                #Creates a save thread which updates it's save_file to the appropriate url folder each 'base_urls' iteration
                kill_save_threads = False
                save_args = (crawled, save_file, kill_save_threads)
                thread_setup(thread_save, 1, function_args=save_args)
                first_url = False
            kill_crawl_threads = False
            crawl_args = (Spider.return_domain_links, queue, crawl_queue, crawled, kill_crawl_threads)
            thread_setup(thread_crawl, NUM_OF_THREADS, function_args=crawl_args)

            #Updates queue
            while len(crawl_queue) > 0:
                #This temp set doesn't allow the original set 'crawl_queue' to change length while being iterated
                temp_crawl_queue = set(crawl_queue)
                already_put = list()
                for retrieved_url in temp_crawl_queue:
                    if retrieved_url not in crawled and retrieved_url not in already_put:
                        already_put.append(retrieved_url)
                        queue.put(retrieved_url)
                crawl_queue = set()
                queue.join()
                print("Finished: Queue.join")

            #Kills crawl threads when finished with this 'base_url' and saves final domain urls
            kill_crawl_threads = True
            container_to_file(crawled, "".join(save_file))

        #Kills save_thread when function ends
        kill_save_threads = True


    @staticmethod
    def load_project(path):
        pass


#Crawling Functions
def thread_setup(function, amount, function_args=None):
    for _ in range(amount):
        t = threading.Thread(target=function, daemon=True, args=function_args)
        t.start()
        print("Initialized {}".format(t.name))

def thread_crawl(spider_function, retrieval_queue, entry_queue, finished_dump=None, kill_var=None):
    while True:
        if kill_var:
            "Deleting {}".format(threading.current_thread().name)
            break
        retrieved_url = retrieval_queue.get()
        retrieved_data = spider_function(retrieved_url)
        for data in retrieved_data:
            #For Sets
            try: entry_queue.add(data)
            #For Lists/Tuples
            except: entry_queue.append(data)
        if finished_dump != None:
            #For Sets
            try: finished_dump.add(retrieved_url)
            #For Lists/Tuples
            except: finished_dump.append(retrieved_url)
        print("queue: {}".format(list(retrieval_queue.queue)))
        try: retrieval_queue.task_done()
        except: pass

def thread_save(save_data, save_file, kill_var=None):
    """Functions which saves crawled data to save_file at an interval of 'SAVE_TIME' seconds"""
    while True:
        sleep(SAVE_TIME)
        if kill_var:
            print("Deleting {}(save_thread)".format(threading.current_thread().name))
            break
        temp_save_data = set(save_data)
        container_to_file(temp_save_data, "".join(save_file))
        print("Crawl data saved to {}".format(save_file[1] + save_file[2]))
        print("Crawl_queue: {}".format(save_data))

crawler = Crawler(Project("Test Project"))
crawler.text_crawl("https://ilovetypography.com", "Gutenberg", True)