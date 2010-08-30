#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import urllib
import re
from datetime import datetime
import xml.etree.cElementTree as ElementTree

import pymongo
from pymongo.objectid import ObjectId
from pymongo import Connection
from config import tag_config


class XmlHandler:
    def __init__(self, url):
        self.url = url
    
    
    def _get_cache_uri(self, url):
        result = url_to_cache.sub(tag_config['cache'], url)
        result = result.replace('/' + tag_config['tmdb']['apikey'], '')
        result = result.replace('/' + tag_config['tvdb']['apikey'], '')
        return result
    
    
    def _cache_url(self, url):
        import os
        local_uri = self._get_cache_uri(url)
        if not os.path.exists(local_uri):
            dirname = os.path.dirname(local_uri)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            urllib.urlretrieve(url, local_uri)
        return local_uri
    
    
    def _grabUrl(self, url):
        value = None
        try:
            local_uri = self._cache_url(url)
            urlhandle = urllib.urlopen(local_uri)
            value = urlhandle.read()
        except IOError, errormsg:
            value = None
        return value
    
    
    def getEt(self):
        et = None
        xml = self._grabUrl(self.url)
        if xml != None:
            try:
                et = ElementTree.fromstring(xml)
            except SyntaxError, errormsg:
                et = None
        return et
    


class EntityManager():
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.tag')
        self.connection = Connection()
        self.db = self.connection[tag_config['db']['name']]
        self.genre_map = None
        
        self.genres = self.db.genres
        self.departments = self.db.departments
        self.jobs = self.db.jobs
        self.networks = self.db.networks
        self.movies = self.db.movies
        self.shows = self.db.shows
        self.seasons = self.db.seasons
        self.episodes = self.db.episodes
        self.people = self.db.people
    
    
    
    def find_network(self, name):
        small_name = name.lower()
        _network = self.networks.find_one({'_id': small_name})
        if _network == None:
            _network = {'_id':small_name, 'name':name}
            self.networks.save(_network)
        return _network
    
    
    def find_job(self, name):
        small_name = name.lower()
        _job = self.jobs.find_one({'_id': small_name})
        if _job == None:
            _job = {'_id':small_name, 'name':name}
            self.jobs.save(_job)
        return _job
    
    
    def find_department(self, name):
        small_name = name.lower()
        _department = self.departments.find_one({'_id': small_name})
        if _department == None:
            _department = {'_id':small_name, 'name':name}
            self.departments.save(_department)
        return _department
    
    
    def find_genre(self, name):
        small_name = name.lower()
        _genre = self.genres.find_one({'_id': small_name})
        if _genre == None:
            _canonic_name = self._map_genre(small_name)
            _genre = self.genres.find_one({'_id': _canonic_name})
            
        if _genre == None:
            _genre = {'_id':small_name, 'name':name}
            self.genres.save(_genre)
            
        return _genre 
    
    
    def find_movie_by_imdb_id(self, imdb_id):
        _movie = self.movies.find_one({"imdb_id": imdb_id})
        if _movie == None:
            _tmdb_id = self._find_tmdb_id_by_imdb_id(imdb_id)
            if _tmdb_id != None:
                _movie = self.find_movie_by_tmdb_id(_tmdb_id)
        return _movie
    
    
    def find_movie_by_tmdb_id(self, tmdb_id):
        _movie = self.movies.find_one({"tmdb_id": tmdb_id})
        if _movie == None:
            _movie = self._update_tmdb_movie(tmdb_id)
        return _movie
    
    
    def find_person_by_tmdb_id(self, tmdb_id):
        _person = self.people.find_one({'tmdb_id':tmdb_id})
        if _person == None:            
            _person = self.update_tmdb_person(tmdb_id)
        return _person
    
    
    def find_show_by_tvdb_id(self, tvdb_id):
        _show = self.shows.find_one({"tvdb_id": tvdb_id})
        if _show == None:
            _show = self._update_tvdb_show_tree(tvdb_id)
        return _show
    
    
    def find_episode_by_tvdb_id(self, key):
        return self.episodes.find_one({'tvdb_id':key})
    
    
    def find_episode(self, show_name, season_number, episode_number):
        return self.episodes.find_one({'small_show_name':show_name.lower(), 'season_number':season_number, 'episode_number':episode_number})
    
    
    
    
    
    def _map_genre(self, name):
        _canonic_name = None
        if self.genre_map == None:
            from config import genre_map as _genre_map
            self.genre_map = []
            for m in _genre_map:
                self.genre_map.append((m[0], re.compile(m[1], re.IGNORECASE)))
        
        index = 0
        while _canonic_name == None and index < len(self.genre_map):
            if self.genre_map[index][1].search(name) != None:
                _canonic_name = self.genre_map[index][0]
            index += 1
        return _canonic_name
    
    
    def _make_genre_item(self, name):
        _genre = self.find_genre(name)
        _genre_ref = dict()
        _genre_ref['id'] = _genre['_id']
        _genre_ref['name'] = _genre['name']
        if 'itmf_code' in _genre:
            _genre_ref['itmf_code'] = _genre['itmf_code']
        return _genre_ref
    
    
    def _update_tmdb_movie(self, tmdb_id):
        _movie = self.movies.find_one({'tmdb_id':tmdb_id})
        url = tag_config['tmdb']['urls']['Movie.getInfo']  % (tmdb_id)
        etree = XmlHandler(url).getEt()
        if etree != None:
            movies_tree = etree.find("movies").findall("movie")
            
            if len(movies_tree) != 0:
                if _movie == None:
                    _movie = {'cast':[], 'genre':[]}
                    
                for item in movies_tree[0].getchildren():
                    if _is_tag('id', item):
                        _update_property('tmdb_id', item.text, _movie)
                        self.movies.save(_movie)
                    elif _is_tag('imdb_id', item):
                        _update_property('imdb_id', item.text, _movie)
                    elif _is_tag('name', item):
                        _update_property('name', item.text, _movie)
                    elif _is_tag('overview', item):
                        _update_property('overview', item.text, _movie)
                    elif _is_tag('tagline', item):
                        _update_property('tagline', item.text, _movie)
                    elif _is_tag('released', item):
                        _update_date_property('released', item.text, _movie)
                    elif _is_tag('certification', item):
                        _update_property('content_rating', item.text, _movie)
                        
                    elif _is_tag('categories', item):
                        _movie['genre'] = list()
                        for category_item in item.getchildren():
                            if  category_item.get('type') == 'genre':
                                _category_name = category_item.get('name')
                                _movie['genre'].append(self._make_genre_item(_category_name))
                                
                    elif _is_tag('cast', item):
                        _movie['cast'] = list()
                        for person_item in item.getchildren():
                            _person_ref = self._make_person_ref(person_item.get('job'), person_item.get('department'), person_item.get('character'), person_item.get('id'), person_item.get('name'))
                            if _person_ref != None:
                                _movie['cast'].append(_person_ref)
                                
                    elif _is_tag('images', item):
                        _movie['image'] = list()
                        for image_item in item.getchildren():
                            if  image_item.get('type') == 'poster':
                                _image_size = image_item.get('size')
                                _image_url = image_item.get('url')
                                #_movie['image'].append(self.make_image_item(...))
                    
                self.movies.save(_movie)
        return _movie
    
    
    def _find_tmdb_id_by_imdb_id(self, imdb_id):
        _tmdb_id = None
        url = tag_config['tmdb']['urls']['Movie.imdbLookup'] % (imdb_id)
        etree = XmlHandler(url).getEt()
        if etree != None:
            movies_tree = etree.find("movies").findall("movie")
            
            if len(movies_tree) != 0:
                for item in movies_tree[0].getchildren():
                    if _is_tag('id', item):
                        _tmdb_id = item.text
        return _tmdb_id
    
    
    def _find_person_by_name(self, name):
        name = collapse_whitespace.sub(' ', name)
        name = name.strip()
        small_name = name.lower()
        _person = None
        if small_name != None and len(small_name) > 0:
            _person = self.people.find_one({'small_name':small_name})
            if _person == None:
                tmdb_person_id = self._find_tmdb_person_id_by_name(name)
                if tmdb_person_id != None:
                    _person = self.find_person_by_tmdb_id(tmdb_person_id)
                else:
                    _person = self._make_person_stub(name)
        return _person
    
    
    def _make_person_stub(self, name):
        _person = {'small_name':name.lower(), 'name':name}
        self.people.save(_person)
        return _person
    
    
    def update_tmdb_person(self, tmdb_id):
        _person = self.people.find_one({'tmdb_id':tmdb_id})
        url = tag_config['tmdb']['urls']['Person.getInfo'] % (tmdb_id)
        etree = XmlHandler(url).getEt()
        if etree != None:
            people_tree = etree.find("people").findall("person")
            
            if len(people_tree) != 0:
                if _person == None:
                    _person = {'filmography':[]}
                    
                for item in people_tree[0].getchildren():
                    if _is_tag('id', item):
                        _update_property('tmdb_id', item.text, _person)
                    elif _is_tag('name', item):
                        _update_property('name', item.text, _person)
                        if item.text != None:
                            _update_property('small_name', item.text.lower(), _person)
                    elif _is_tag('birthday', item):
                        _update_date_property('birthday', item.text, _person)
                    elif _is_tag('deathday', item):
                        _update_date_property('deathday', item.text, _person)
                    elif _is_tag('biography', item) and item.text != None:
                        _update_property('biography', item.text, _person)
                        
                    elif _is_tag('filmography', item):
                        _person['filmography'] = list()
                        for movie_item in item.getchildren():
                            _movie_ref = self._make_movie_ref(movie_item.get('job'), movie_item.get('department'), movie_item.get('id'), movie_item.get('name'), movie_item.get('character'))
                            if _movie_ref != None:
                                _person['filmography'].append(_movie_ref)
                            
                self.people.save(_person)
        return _person
    
    
    def _find_tmdb_person_id_by_name(self, name):
        result = None
        name = collapse_whitespace.sub(' ', name)
        url = tag_config['tmdb']['urls']['Person.search'] % (_prepare_for_tmdb_query(name))
        etree = XmlHandler(url).getEt()
        if etree != None:
            people_tree = etree.find("people").findall("person")
            for person_item in people_tree:
                is_match = False
                tmdb_id = None
                for item in person_item.getchildren():
                    if _is_tag('name', item):
                        if item.text.lower() == name.lower():
                            is_match = True
                    elif _is_tag('id', item):
                        tmdb_id = item.text
                if is_match:
                    result = tmdb_id
                    break
        return result
    
    
    def _make_person_ref(self, job, department, character=None, person_tmdb_id=None, person_name=None):
        _person_ref = None
        _person = None
        _department = self.find_department(department)
        _job = self.find_job(job)
        if person_tmdb_id != None:
            _person = self.find_person_by_tmdb_id(person_tmdb_id)
        
        if _person == None:
            _person = self._find_person_by_name(person_name)
            
        if _person != None:
            _person_ref = dict()
            _person_ref['id'] = _person['_id']
            if 'tmdb_id' in _person:
                _update_property('tmdb_id', _person['tmdb_id'], _person_ref)
            _update_property('name', _person['name'], _person_ref)
            _update_property('character', character, _person_ref)
            _update_property('department', _department['_id'], _person_ref)
            _update_property('job', _job['_id'], _person_ref)
        return _person_ref
    
    
    def _make_movie_ref(self, job, department, movie_tmdb_id, movie_name, character=None):
        _movie_ref = None
        _department = self.find_department(department)
        _job = self.find_job(job)
        
        if movie_tmdb_id != None and movie_name != None:
            _movie_ref = dict()
            _update_property('name', movie_name, _movie_ref)
            _update_property('id', movie_tmdb_id, _movie_ref)
            _update_property('job', _job['_id'], _movie_ref)
            _update_property('department', _department['_id'], _movie_ref)
            _update_property('character', character, _movie_ref)
        return _movie_ref
    
    
    def _update_tvdb_show_tree(self, tvdb_id):
        url = tag_config['tvdb']['urls']['Show.getInfo'] % (tvdb_id)
        etree = XmlHandler(url).getEt()
        _show = self._update_tvdb_show(tvdb_id, etree)
        self._update_tvdb_episodes(_show, etree)
        return _show
    
    
    def _update_tvdb_show(self, tvdb_id, etree):
        _show = self.shows.find_one({'tvdb_id':tvdb_id})
        show_nodes = etree.findall("Series")
        if len(show_nodes) != 0:
            if _show == None:
                _show = {'genre':[], 'cast':[]}
            else:
                _show['genre'] = []
                _show['cast'] = []
                
            for item in show_nodes[0].getchildren():
                if _is_tag('id', item):
                    _update_property('tvdb_id', item.text, _show)
                elif _is_tag('IMDB_ID', item):
                    _update_property('imdb_id', item.text, _show)
                elif _is_tag('SeriesName', item):
                    _update_property('name', item.text, _show)
                elif _is_tag('Overview', item):
                    _update_property('overview', item.text, _show)
                elif _is_tag('ContentRating', item):
                    _update_property('content_rating', item.text, _show)
                elif _is_tag('Network', item):
                    _network = self.find_network(item.text)
                    _update_property('network_id', _network['_id'], _show)
                    _update_property('network', _network['name'], _show)
                elif _is_tag('Genre', item):
                    _show['genre'] = list()
                    genre_list = _split_tvdb_list(item.text)
                    for g in genre_list:
                        _show['genre'].append(self._make_genre_item(g))
                elif _is_tag('Actors', item):
                    _show['cast'] = list()
                    actor_list = _split_tvdb_list(item.text)
                    for actor in actor_list:
                        _person_ref = self._make_person_ref(job='actor', department='actors', person_name=actor)
                        if _person_ref != None:
                            _show['cast'].append(_person_ref)
                            
            self.shows.save(_show)
        return _show
    
    
    def _update_tvdb_episodes(self, show, etree):
        episode_nodes = etree.findall("Episode")
        if len(episode_nodes) != 0:
            small_show_name = show['name'].lower()
            for episode_item in episode_nodes:
                _tvdb_episode_id = episode_item.find('id').text
                _episode = self.episodes.find_one({'tvdb_id':_tvdb_episode_id})
                if _episode == None:
                    _episode = {'cast':[]}
                else:
                    _episode['cast'] = list()
                    
                _episode['small_show_name'] = small_show_name
                for item in episode_item.getchildren():
                    if _is_tag('id', item):
                        _update_property('tvdb_id', item.text, _episode)
                    elif _is_tag('seriesid', item):
                        _update_property('show_tvdb_id', item.text, _episode)
                    elif _is_tag('seasonid', item):
                        _update_property('season_tvdb_id', item.text, _episode)
                    elif _is_tag('IMDB_ID', item):
                        _update_property('imdb_id', item.text, _episode)
                    elif _is_tag('EpisodeName', item):
                        _update_property('name', item.text, _episode)
                    elif _is_tag('EpisodeNumber', item):
                        _update_property('episode_number', item.text, _episode)
                    elif _is_tag('SeasonNumber', item):
                        _update_property('season_number', item.text, _episode)
                    elif _is_tag('Overview', item):
                        _update_property('overview', item.text, _episode)
                    elif _is_tag('ProductionCode', item):
                        _update_property('production_code', item.text, _episode)
                    elif _is_tag('FirstAired', item):
                        _update_date_property('released', item.text, _episode)
                    elif _is_tag('Director', item):
                        director_list = _split_tvdb_list(item.text)
                        for director in director_list:
                            _person_ref = self._make_person_ref(job='director', department='directing', person_name=director)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                    elif _is_tag('Writer', item):
                        writer_list = _split_tvdb_list(item.text)
                        for writer in writer_list:
                            _person_ref = self._make_person_ref(job='screenplay', department='writing', person_name=writer)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                    elif _is_tag('GuestStars', item):
                        actor_list = _split_tvdb_list(item.text)
                        for actor in actor_list:
                            _person_ref = self._make_person_ref(job='actor', department='actors', person_name=actor)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                                
                self.episodes.save(_episode)
    
    




def _is_tag(name, item):
    result = False
    if item.tag == name:
        result = True
    return result


def _update_property(key, value, entity):
    result = False
    old_value = None
    if key in entity:
        old_value = entity[key]
        
    if value != None:
        value = value.strip()
        if len(value) == 0:
            value = None
            
    if old_value != value:
        result = True
        if value == None:
            del entity[key]
        else:
            entity[key] = value
    return result


def _update_date_property(key, value, entity):
    result = False
    old_value = None
    if key in entity:
        old_value = entity[key]
        
    if value != None:
        value = value.strip()
        if len(value) != 0 and valid_tmdb_date.search(value) != None:
            value = datetime.strptime(value, "%Y-%m-%d")
        else:
            value = None
            
    if old_value != value:
        result = True
        if value == None:
            del entity[key]
        else:
            entity[key] = value
    return result


def _split_tvdb_list(value):
    result = list()
    if value != None:
        value = tvdb_list_seperators.sub('|', value)
        value = strip_space_around_seperator.sub('|', value)
        value = value.strip().strip('|')
        if len(value) > 0:
            result = value.split('|')
    return result


def _prepare_for_tmdb_query(value):
    result = None
    if value != None:
        value = value.strip()
        value = value.encode('utf8')
        value = collapse_whitespace.sub('+', value)
    return value


valid_tmdb_date = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
tvdb_list_seperators = re.compile(r'\||,')
strip_space_around_seperator = re.compile(r'\s*\|\s*')
collapse_whitespace = re.compile(r'\s+')
url_to_cache = re.compile(r'http://')
