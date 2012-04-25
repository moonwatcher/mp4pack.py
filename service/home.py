# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

class HomeHandler(ResourceHandler):
    def __init__(self, node):
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        # create an empty record
        pass
    
    
    def parse(self, query):
        # update the indexs
        pass
    

