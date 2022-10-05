import json
import requests
import logging

class MovieClient(object):

    def __init__(self,APIKEY,BASEURL):

        self.key = APIKEY
        self.baseURL = BASEURL

    def getReq(self,url):
        try:
            res = requests.get(url)
            return res
        except:
            logging.info("error in get request")
