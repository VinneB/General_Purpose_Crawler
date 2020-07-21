#This module is contains the source for the customizable crawler
from bs4 import BeautifulSoup
import time
import queue
import threading
from urllib.request import urlopen
import requests
from threading import Thread
from urllib import parse
from dull_functions import remove_duplicates, get_domain_name

ALLOWED_DATA_TYPES = ["text/html; charset=UTF-8", "text/html; charset=utf-8", "text/html;charset=utf-8", "text/html;charset=UTF-8"]

class Spider:
    def __init__(self, url):
        """Notes: In all functions, tags and attributes can be single items or lists"""
        print("First Spider searching base url for links")
        self.base_page_links = Spider.return_all_links(url)

    @staticmethod
    def return_specified_text(url, text):
        """Searches webpage for text instances of any of the specified text. Returns all instances
        Note: Text only needs to possess one of the specified texts"""
        return_tags = set()
        if isinstance(text, str): text = [text]
        source = BeautifulSoup(Spider.get_raw_html(url), 'lxml').find_all()
        for tag in source:
            for text_instance in text:
                if text_instance in tag.text:
                    return_tags.add(tag.text)
        return remove_duplicates(return_tags)

    @staticmethod
    def return_specified_text_specific(url, text):
        return_tags = list()
        if isinstance(text, str): text = [text]
        #Finds all tags in html
        source = BeautifulSoup(Spider.get_raw_html(url), "lxml").find_all()
        #Adds tags that have any of the text_instances into 'tags' similar to 'return_specified_text'
        for tag in source:
            for text_instance in text:
                if text_instance in tag.text:
                    return_tags.append(tag.text)
        #Takes any tag that doesn't contain all of the text instances out of 'tags'
        for tag_text in range(len(return_tags)):
            for text_instance in text:
                if text_instance not in return_tags[tag_text]:
                    return_tags.pop(tag_text)
        return remove_duplicates(return_tags)


    @staticmethod
    def return_all_links(url):
        """Gathers all the 'a' tags in the 'url' source code and returns all the 'a' tag texts
         and 'href' values in a tuple"""
        links = set()
        source = BeautifulSoup(Spider.get_raw_html(url), "lxml")
        a_tags = source.find_all("a")
        for tag in a_tags:
            if "/" in tag.get("href"):
                links.add((tag.text, tag.get("href")))

        return remove_duplicates(links)

    @staticmethod
    def return_custom(url, search_tags, search_attributes=None):
        """Searches the 'url' source code and returns the specified tags. If any attributes are specified,
         then it will return only tags with those attributes
         Notes: Attributes must be a dict."""
         #Neccessary vars
        return_tags = list()
        if isinstance(search_tags, str): search_tags = [search_tags]
        accepted_tags = list()
        source = BeautifulSoup(Spider.get_raw_html(url), "lxml")
        #Adds specified tags
        for tag in search_tags:
            accepted_tags.extend(source.find_all(tag))
        if search_attributes != None:
            #Filters out tags without the specified attributes
            for (attr, val) in search_attributes.items():
                for tag in accepted_tags:
                    if val in tag.get_attribute_list(attr):
                        return_tags.append(tag)
            return set(return_tags)
        return remove_duplicates(accepted_tags)
                        

    @staticmethod
    def get_raw_html(url):
        """Makes a get request to 'url'"""
        #Trys to get a response form website. If the response is in the ALLOWED_DATA_TYPES, then it returns the html
        try:
            response = requests.get(url)
            if response.headers["Content-Type"] in ALLOWED_DATA_TYPES:
                return response.text
            print("Error: Illegal file type")
            return ''
        except:
            print("Error: Couldn't crawl {}".format(url))
            return ''

    @staticmethod
    def return_domain_links(url):
        domain_links = list()
        domain = get_domain_name(url)
        links = Spider.return_all_links(url)
        for link in links:
            if domain in link:
                domain_links.append(link[1])
        return domain_links
