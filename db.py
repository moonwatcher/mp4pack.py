#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import logging
import urllib
from datetime import datetime
import xml.etree.cElementTree as ElementTree

import pymongo
from pymongo.objectid import ObjectId
from pymongo import Connection
from config import tag_config


class ResourceHandler(object):
    def __init__(self, url):
        self.logger = logging.getLogger('mp4pack.resource')
        self.remote_url = url
        self.local_path = self.local_path_from_remote_url()
        self.headers = None
    
    
    def local_path_from_remote_url(self):
        return url_to_cache.sub(tag_config['cache'], self.remote_url)
    
    
    def cache(self):
        result = True
        if not os.path.exists(self.local_path):
            dirname = os.path.dirname(self.local_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            try:
                filename, self.headers = urllib.urlretrieve(self.remote_url, self.local_path)
            except IOError:
                result = False
                self.logger.error('failed to retrieve ' + self.remote_url)
        return result
    
    
    def read(self):
        value = None
        try:
            if self.cache():
                urlhandle = urllib.urlopen(self.local_path)
                value = urlhandle.read()
        except IOError:
            value = None
            self.logger.error('failed to read ' + self.local_path)
        return value
    
    


class JsonHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.json')
    
    
    def get_element(self):
        element = None
        json_text = self.read()
        if json_text != None:
            try:
                from StringIO import StringIO
                io = StringIO(json_text)
                import json
                element = json.load(io)
            except ValueError:
                element = None
                self.logger.error('failed to load json document ' + self.local_path)
        return element
    


class XmlHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.xml')
    
    
    def get_element(self):
        element = None
        xml = self.read()
        if xml != None:
            try:
                element = ElementTree.fromstring(xml)
            except SyntaxError:
                self.logger.error('failed to load xml document ' + self.local_path)
                os.remove(self.local_path)
                try:
                    os.removedirs(os.path.dirname(self.local_path))
                except OSError:
                    pass
                element = None
        return element
    


class TmdbJsonHandler(JsonHandler):
    def __init__(self, url):
        JsonHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.json.tmdb')
    
    
    def local_path_from_remote_url(self):
        result = ResourceHandler.local_path_from_remote_url(self)
        result = result.replace('/' + tag_config['tmdb']['apikey'], '')
        return result
    
    
    def get_element(self):
        element = JsonHandler.get_element(self)
        if element == None or len(element) == 0 or element[0] == 'Nothing found.':
            self.logger.warning('Nothing found in ' + self.remote_url)
            os.remove(self.local_path)
            try:
                os.removedirs(os.path.dirname(self.local_path))
            except OSError:
                pass
            element = None
        return element
    
    


class TvdbXmlHandler(XmlHandler):
    def __init__(self, url):
        XmlHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.xml.tvdb')
    
    
    def local_path_from_remote_url(self):
        result = ResourceHandler.local_path_from_remote_url(self)
        result = result.replace('/' + tag_config['tvdb']['apikey'], '')
        result = result.replace('/all', '')
        return result
    
    


class TvdbImageHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.image.tvdb')
    
    
    def cache(self):
        ResourceHandler.cache(self)


class TagManager(object):
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
        _movie = self.movies.find_one({'imdb_id': imdb_id})
        if _movie == None:
            _tmdb_id = self._find_tmdb_id_by_imdb_id(imdb_id)
            if _tmdb_id != None:
                _movie = self.find_movie_by_tmdb_id(_tmdb_id)
        return _movie
    
    
    def find_movie_by_tmdb_id(self, tmdb_id):
        _movie = self.movies.find_one({'tmdb_id': tmdb_id})
        if _movie == None:
            _movie = self._update_tmdb_movie(tmdb_id)
        return _movie
    
    
    def find_person_by_tmdb_id(self, tmdb_id):
        _person = self.people.find_one({'tmdb_id':tmdb_id})
        if _person == None:            
            _person = self.update_tmdb_person(tmdb_id)
        return _person
    
    
    def find_show_by_tvdb_id(self, tvdb_id):
        _show = self.shows.find_one({'tvdb_id': tvdb_id})
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
        handler = TmdbJsonHandler(url)
        element = handler.get_element()
        if element != None:
            element = element[0]
            if _movie == None:
                _movie = {'cast':[], 'genre':[], 'posters':[]}
                
            update_int_property('tmdb_id', element['id'], _movie)
            self.movies.save(_movie)
            update_int_property('imdb_id', element['imdb_id'], _movie)
            update_string_property('name', element['name'], _movie)
            update_string_property('overview', element['overview'], _movie)
            update_string_property('tagline', element['tagline'], _movie)
            update_string_property('content_rating', element['certification'], _movie)
            update_date_property('released', element['released'], _movie)
            
            if 'genres' in element.keys():
                _movie['genre'] = list()
                for ge in element['genres']:
                    if ge['type'] == 'genre':
                        _movie['genre'].append(self._make_genre_item(ge['name']))
                        
            if 'cast' in element.keys():
                _movie['cast'] = list()
                for ce in element['cast']:
                    _person_ref = self._make_person_ref_from_element(ce)
                    if _person_ref != None:
                        _movie['cast'].append(_person_ref)
                                    
            #if 'posters' in element.keys():
            #    _movie['posters'] = list()
            #    for pe in element['posters']:
                    
            self.movies.save(_movie)
        return _movie
    
    
    def _find_tmdb_id_by_imdb_id(self, imdb_id):
        _tmdb_id = None
        url = tag_config['tmdb']['urls']['Movie.imdbLookup'] % (imdb_id)
        handler = TmdbJsonHandler(url)
        element = handler.get_element()
        if element != None:
            element = element[0]
            _tmdb_id = element['id']
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
        handler = TmdbJsonHandler(url)
        element = handler.get_element()
        if element != None:
            element = element[0]
            if _person == None:
                _person = {'filmography':[]}
            update_int_property('tmdb_id', element['id'], _person)
            update_string_property('name', element['name'], _person)
            update_string_property('small_name', element['name'].lower(), _person)
            update_date_property('birthday', element['birthday'], _person)
            update_string_property('biography', element['biography'], _person)
            
            if 'filmography' in element.keys():
                _person['filmography'] = list()
                for fe in element['filmography']:
                    _movie_ref = self._make_movie_ref_from_element(fe)
                    if _movie_ref != None:
                        _person['filmography'].append(_movie_ref)
            self.people.save(_person)
        return _person
    
    
    def _find_tmdb_person_id_by_name(self, name):
        result = None
        name = collapse_whitespace.sub(' ', name)
        url = tag_config['tmdb']['urls']['Person.search'] % (prepare_for_tmdb_query(name))
        handler = TmdbJsonHandler(url)
        element = handler.get_element()
        if element != None:
            for pe in element:
                if pe['name'].lower() == name.lower():
                    result = pe['id']
                    break
        return result
    
    
    def _make_person_ref_from_element(self, element):
        return self._make_person_ref(element['job'], element['department'], element['character'], element['id'], element['name'])
    
    
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
                update_int_property('tmdb_id', _person['tmdb_id'], _person_ref)
            update_string_property('name', _person['name'], _person_ref)
            update_string_property('character', character, _person_ref)
            update_string_property('department', _department['_id'], _person_ref)
            update_string_property('job', _job['_id'], _person_ref)
        return _person_ref
    
    
    def _make_movie_ref_from_element(self, element):
        return self._make_movie_ref(element['job'], element['department'], element['id'], element['name'], element['character'])
    
    
    def _make_movie_ref(self, job, department, movie_tmdb_id, movie_name, character=None):
        _movie_ref = None
        _department = self.find_department(department)
        _job = self.find_job(job)
        
        if movie_tmdb_id != None and movie_name != None:
            _movie_ref = dict()
            update_string_property('name', movie_name, _movie_ref)
            update_int_property('id', movie_tmdb_id, _movie_ref)
            update_string_property('job', _job['_id'], _movie_ref)
            update_string_property('department', _department['_id'], _movie_ref)
            update_string_property('character', character, _movie_ref)
        return _movie_ref
    
    
    def _update_tvdb_show_tree(self, tvdb_id):
        url = tag_config['tvdb']['urls']['Show.getInfo'] % (tvdb_id)
        element = TvdbXmlHandler(url).get_element()
        _show = self._update_tvdb_show(tvdb_id, element)
        self._update_tvdb_episodes(_show, element)
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
                if is_tag('id', item):
                    update_int_property('tvdb_id', int(item.text), _show)
                elif is_tag('IMDB_ID', item):
                    update_string_property('imdb_id', item.text, _show)
                elif is_tag('SeriesName', item):
                    update_string_property('name', item.text, _show)
                elif is_tag('Overview', item):
                    update_string_property('overview', item.text, _show)
                elif is_tag('ContentRating', item):
                    update_string_property('content_rating', item.text, _show)
                elif is_tag('Network', item):
                    _network = self.find_network(item.text)
                    update_string_property('network_id', _network['_id'], _show)
                    update_string_property('network', _network['name'], _show)
                elif is_tag('Genre', item):
                    _show['genre'] = list()
                    genre_list = split_tvdb_list(item.text)
                    for g in genre_list:
                        _show['genre'].append(self._make_genre_item(g))
                elif is_tag('Actors', item):
                    _show['cast'] = list()
                    actor_list = split_tvdb_list(item.text)
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
                _tvdb_episode_id = int(episode_item.find('id').text)
                _episode = self.episodes.find_one({'tvdb_id':_tvdb_episode_id})
                if _episode == None:
                    _episode = {'cast':[]}
                else:
                    _episode['cast'] = list()
                    
                _episode['small_show_name'] = small_show_name
                for item in episode_item.getchildren():
                    if is_tag('id', item):
                        update_int_property('tvdb_id', int(item.text), _episode)
                    elif is_tag('seriesid', item):
                        update_int_property('show_tvdb_id', int(item.text), _episode)
                    elif is_tag('seasonid', item):
                        update_int_property('season_tvdb_id', int(item.text), _episode)
                    elif is_tag('IMDB_ID', item):
                        update_string_property('imdb_id', item.text, _episode)
                    elif is_tag('EpisodeName', item):
                        update_string_property('name', item.text, _episode)
                    elif is_tag('EpisodeNumber', item):
                        update_int_property('episode_number', int(item.text), _episode)
                    elif is_tag('SeasonNumber', item):
                        update_int_property('season_number', int(item.text), _episode)
                    elif is_tag('Overview', item):
                        update_string_property('overview', item.text, _episode)
                    elif is_tag('ProductionCode', item):
                        update_string_property('production_code', item.text, _episode)
                    elif is_tag('FirstAired', item):
                        update_date_property('released', item.text, _episode)
                    elif is_tag('Director', item):
                        director_list = split_tvdb_list(item.text)
                        for director in director_list:
                            _person_ref = self._make_person_ref(job='director', department='directing', person_name=director)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                    elif is_tag('Writer', item):
                        writer_list = split_tvdb_list(item.text)
                        for writer in writer_list:
                            _person_ref = self._make_person_ref(job='screenplay', department='writing', person_name=writer)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                    elif is_tag('GuestStars', item):
                        actor_list = split_tvdb_list(item.text)
                        for actor in actor_list:
                            _person_ref = self._make_person_ref(job='actor', department='actors', person_name=actor)
                            if _person_ref != None:
                                _episode['cast'].append(_person_ref)
                                
                self.episodes.save(_episode)
    
    




def is_tag(name, item):
    result = False
    if item.tag == name:
        result = True
    return result


def update_int_property(key, value, entity):
    result = False
    old_value = None
    if key in entity:
        old_value = entity[key]
        
    if old_value != value:
        result = True
        if value == None:
            del entity[key]
        else:
            entity[key] = value
    return result


def update_string_property(key, value, entity):
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


def update_date_property(key, value, entity):
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


def split_tvdb_list(value):
    result = list()
    if value != None:
        value = tvdb_list_seperators.sub('|', value)
        value = strip_space_around_seperator.sub('|', value)
        value = value.strip().strip('|')
        if len(value) > 0:
            result = value.split('|')
    return result


def prepare_for_tmdb_query(value):
    result = None
    if value != None:
        value = value.strip().lower()
        value = value.encode('utf8')
        value = collapse_whitespace.sub('+', value)
    return value


valid_tmdb_date = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}')
tvdb_list_seperators = re.compile(r'\||,')
strip_space_around_seperator = re.compile(r'\s*\|\s*')
collapse_whitespace = re.compile(r'\s+')
url_to_cache = re.compile(r'http://')
