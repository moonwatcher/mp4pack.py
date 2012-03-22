# -*- coding: utf-8 -*-

import json
from StringIO import StringIO
from urllib2 import Request, urlopen, URLError, HTTPError

class KnowlegeBaseHandler(ResourceHandler):
    def __init__(self, node):
        ResourceHandler.__init__(self, node)
    
    
    def fetch(self, query):
        pass
    
    
    def parse(self, query):
        pass
    

