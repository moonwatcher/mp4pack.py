# -*- coding: utf-8 -*-

class Album(object):
    def __init__(self, ontology):
        self.ontology = ontology
        

class Disc(object):
    def __init__(self, ontology):
        self.ontology = ontology
        
    @property
    def album(self):
        pass
        

class Track(object):
    def __init__(self, ontology):
        self.ontology = ontology
        
    @property
    def disc(self):
        pass
        
    @property
    def album(self):
        pass
        

class Show(Album):
    def __init__(self, ontology):
        Album.__init__(self, ontology)
        

class Season(Disc):
    def __init__(self, ontology):
        Disc.__init__(self, ontology)
        
    @property
    def show(self):
        return self.album
        

class Episode(Track):
    def __init__(self, ontology):
        Track.__init__(self, ontology)
        
    @property
    def season(self):
        return self.disc
        
    @property
    def show(self):
        return self.album
        

class Movie(Track):
    def __init__(self, ontology):
        Track.__init__(self, ontology)
        

class Person(object):
    def __init__(self, ontology):
        self.ontology = ontology
        

class Network(object):
    def __init__(self, ontology):
        self.ontology = ontology
        

class Studio(object):
    def __init__(self, ontology):
        self.ontology = ontology
        

