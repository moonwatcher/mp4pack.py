#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import logging
import urllib
import unicodedata
from datetime import datetime
import xml.etree.cElementTree as ElementTree

import pymongo
from pymongo.objectid import ObjectId
from pymongo import Connection

from config import repository_config


class ResourceHandler(object):
    def __init__(self, url):
        self.logger = logging.getLogger('mp4pack.resource')
        self.remote_url = url
        self.local_path = self.local()
        self.headers = None
    
    
    def local(self):
        return url_to_cache.sub(repository_config['Database']['cache'], self.remote_url)
    
    
    def cache(self):
        result = True
        if not os.path.exists(self.local_path):
            dirname = os.path.dirname(self.local_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            try:
                self.logger.info(u'Retrieve %s', self.remote_url)
                filename, self.headers = urllib.urlretrieve(self.remote_url.encode('utf-8'), self.local_path)
            except IOError:
                result = False
                self.clean()
                self.logger.warning(u'Failed to retrieve %s', self.remote_url)
        return result
    
    
    def read(self):
        value = None
        try:
            if self.cache():
                urlhandle = urllib.urlopen(self.local_path.encode('utf-8'))
                value = urlhandle.read()
        except IOError:
            value = None
            self.logger.warning(u'Failed to read %s', self.local_path)
        return value
    
    
    def clean(self):
        if os.path.isfile(self.local_path):
            os.remove(self.local_path)
            try:
                os.removedirs(os.path.dirname(self.local_path))
            except OSError:
                pass
    
    


class JsonHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.json')
    
    
    def element(self):
        element = None
        json_text = self.read()
        if json_text is not None:
            try:
                from StringIO import StringIO
                io = StringIO(json_text)
                import json
                element = json.load(io)
            except ValueError:
                element = None
                self.clean()
                self.logger.error(u'Failed to load json document %s', self.local_path)
        return element
    


class ImageHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.image')
    
    
    def cache(self):
        result = ResourceHandler.cache(self)
        if self.headers is not None and image_http_type.search(self.headers.type) is None:
            self.clean()
            result = False
        return result
    
    


class XmlHandler(ResourceHandler):
    def __init__(self, url):
        ResourceHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.xml')
    
    
    def element(self):
        element = None
        xml = self.read()
        if xml is not None:
            try:
                element = ElementTree.fromstring(xml)
            except SyntaxError:
                element = None
                self.clean()
                self.logger.warning(u'Failed to load xml document %s', self.local_path)
        return element
    


class TmdbJsonHandler(JsonHandler):
    def __init__(self, url):
        JsonHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.tmdb')
    
    
    def local(self):
        result = ResourceHandler.local(self)
        result = result.replace(u'/{0}'.format(repository_config['Database']['tmdb']['apikey']), u'')
        return result
    
    
    def element(self):
        element = JsonHandler.element(self)
        if not element or element[0] == u'Nothing found.':
            element = None
            self.clean()
            self.logger.warning(u'Nothing found in %s', self.remote_url)
        return element
    
    


class TvdbXmlHandler(XmlHandler):
    def __init__(self, url):
        XmlHandler.__init__(self, url)
        self.logger = logging.getLogger('mp4pack.tvdb')
    
    
    def local(self):
        result = ResourceHandler.local(self)
        result = result.replace(u'/{0}'.format(repository_config['Database']['tvdb']['apikey']), u'')
        result = result.replace(u'/all', u'')
        return result
    
    


class TvdbImageHandler(ImageHandler):
    def __init__(self, url):
        ImageHandler.__init__(self, repository_config['Database']['tvdb']['urls']['Banner.getImage'].format(url))
        self.logger = logging.getLogger('mp4pack.image')
    
    



class EntityManager(object):
    def __init__(self):
        self.logger = logging.getLogger('mp4pack.em')
        self.connection = Connection(repository_config['Database']['uri'])
        self.db = self.connection[repository_config['Database']['name']]
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
    
    
    def base_init(self):
        from config import base_config
        for g in base_config['genre']:
            self.insert_genre(g)
        
        for s in base_config['tvshow']:
            self.map_show(s[1], s[0])
    
    
    def find_network(self, name):
        small_name = name.lower()
        _network = self.networks.find_one({u'_id': small_name})
        if _network is None:
            _network = {u'_id':small_name, u'name':name}
            self.networks.save(_network)
            self.logger.info(u'Creating TV Network %s', name)
        return _network
    
    
    def find_job(self, name):
        small_name = name.lower()
        _job = self.jobs.find_one({u'_id': small_name})
        if _job is None:
            _job = {u'_id':small_name, u'name':name}
            self.jobs.save(_job)
            self.logger.info(u'Creating Job %s', name)
        return _job
    
    
    def find_department(self, name):
        small_name = name.lower()
        _department = self.departments.find_one({u'_id': small_name})
        if _department is None:
            _department = {u'_id':small_name, u'name':name}
            self.departments.save(_department)
            self.logger.info(u'Creating Department %s', name)
        return _department
    
    
    def find_genre(self, name):
        small_name = name.lower()
        _genre = self.genres.find_one({u'_id': small_name})
        if _genre is None:
            _canonic_name = self._map_genre(small_name)
            _genre = self.genres.find_one({u'_id': _canonic_name})
            
        if _genre is None:
            _genre = self.make_genre(name)
        return _genre 
    
    
    def find_movie_by_imdb_id(self, imdb_id):
        _movie = self.movies.find_one({u'imdb_id': imdb_id})
        if _movie is None:
            _tmdb_id = self._find_tmdb_id_by_imdb_id(imdb_id)
            if _tmdb_id is not None:
                _movie = self.find_movie_by_tmdb_id(_tmdb_id)
        return _movie
    
    
    def find_movie_by_tmdb_id(self, tmdb_id):
        _movie = self.movies.find_one({u'tmdb_id': tmdb_id})
        if _movie is None:
            _movie = self.update_tmdb_movie(tmdb_id)
        return _movie
    
    
    def find_person_by_tmdb_id(self, tmdb_id):
        _person = self.people.find_one({u'tmdb_id':tmdb_id})
        if _person is None:            
            _person = self.update_tmdb_person(tmdb_id)
        return _person
    
    
    def find_show_by_tvdb_id(self, tvdb_id):
        _show = self.shows.find_one({u'tvdb_id': tvdb_id})
        if _show is None:
            _show = self.update_tvdb_show_tree(tvdb_id)
        return _show
    
    
    def find_episode_by_tvdb_id(self, key):
        return self.episodes.find_one({u'tvdb_id':key})
    
    
    
    def map_show_with_pair(self, pair):
        if pair is not None:
            match = numberic_key_string_pair.search(pair)
            if match is not None:
                self.map_show(match.group(2), int(match.group(1)))
            else:
                self.logger.error(u'Could not parse %s', pair)
    
    
    def map_show(self, small_name, tvdb_id):
        show_by_tvdb_id = self.shows.find_one({u'tvdb_id':tvdb_id})
        show_by_small_name = self.shows.find_one({u'small_name':small_name})
        
        if show_by_small_name is None and show_by_tvdb_id is None:
            # This is good, we can do the mapping
            show = {u'small_name':small_name, u'tvdb_id':tvdb_id, u'last_update':None}
            self.shows.save(show)
            self.logger.info(u'Show %s is now mapped to TVDB ID %d', small_name, tvdb_id)
        
        else: # This means at least one exists
            if not(show_by_small_name is not None and show_by_tvdb_id is not None and show_by_tvdb_id[u'_id'] == show_by_small_name[u'_id']):
                if show_by_small_name is not None:
                    self.logger.error(u'Show %s is already mapped to TVDB ID %d', small_name, show_by_small_name[u'tvdb_id'])
            
                if show_by_tvdb_id is not None:
                    self.logger.error(u'Show %s is already mapped to TVDB ID %d', show_by_tvdb_id[u'small_name'], tvdb_id)
            elif show_by_small_name is not None and show_by_tvdb_id is not None and show_by_tvdb_id[u'_id'] == show_by_small_name[u'_id']:
                self.logger.warning(u'Show %s to TVDB ID %d mapping exists', show_by_tvdb_id[u'small_name'], tvdb_id)
        
    
    
    def find_show(self, small_name):
        show = self.shows.find_one({u'small_name': small_name})
        if show is not None:
            if show[u'last_update'] is None and u'tvdb_id' in show:
                self.logger.info(u'Updating show %s', small_name)
                self.update_tvdb_show_tree(show[u'tvdb_id'])
                self.logger.info(u'Done updating show %s', small_name)
        else:
            self.logger.error(u'Show %s does not exist', small_name)
        return show
    
    
    def find_episode(self, show_small_name, season_number, episode_number):
        show = self.find_show(show_small_name)
        episode = None
        if show is not None:
            episode = self.episodes.find_one({u'show_small_name':show_small_name, u'season_number':season_number, u'episode_number':episode_number})
        return show, episode
    
    
    def find_tmdb_movie_poster(self, imdb_id):
        poster = None
        _movie = self.find_movie_by_imdb_id(imdb_id)
        if _movie is not None and _movie['posters']:
            poster = [ p for p in _movie[u'posters'] if 'selected' in p and p['selected'] == True]
            if poster: poster = poster[0]
            if poster and 'url' in poster:
                ih = ImageHandler(poster['url'])
                if ih.cache():
                    poster['local'] = ih.local()
                    poster['kind'] = os.path.splitext(poster['local'])[1].strip('.')
                else:
                    poster = None
        return poster
    
    
    def find_tvdb_episode_poster(self, show_small_name, season_number, episode_number):
        poster = None
        show, _episode = self.find_episode(show_small_name, season_number, episode_number)
        if _episode is not None and 'poster' in _episode:
            ih = TvdbImageHandler(_episode['poster'])
            if ih.cache():
                poster = {'local':ih.local()}
                poster['kind'] = os.path.splitext(poster['local'])[1].strip('.')
            else:
                poster = None
        return poster
    
    
    
    def insert_genre(self, genre):
        result = None
        result = self.genres.find_one({u'_id': genre[u'_id']})
        if result is None:
            self.genres.save(genre)
            result = genre
            if u'itmf' in genre.keys():
                self.logger.info(u'Creating genre %s with iTMF code %d', genre[u'name'], genre[u'itmf'])
            else:
                self.logger.info(u'Creating genre %s', genre[u'name'])
        return result
    
    
    def make_genre(self, name, itmf=None, small_name=None):
        result = None
        if small_name is None:
            small_name = name.lower()
        result = {u'_id':small_name, u'name':name}
        if itmf is not None:
            result[u'itmf'] = itmf
        result = self.insert_genre(result)
        return result
    
    
    def _map_genre(self, name):
        _canonic_name = None
        if self.genre_map is None:
            from config import genre_map as _genre_map
            self.genre_map = []
            for m in _genre_map:
                self.genre_map.append((m[0], re.compile(m[1], re.IGNORECASE)))
        
        index = 0
        while _canonic_name is None and index < len(self.genre_map):
            if self.genre_map[index][1].search(name) is not None:
                _canonic_name = self.genre_map[index][0]
            index += 1
        return _canonic_name
    
    
    def _make_genre_item(self, name):
        _genre = self.find_genre(name)
        _genre_ref = {}
        _genre_ref[u'id'] = _genre[u'_id']
        _genre_ref[u'name'] = _genre[u'name']
        if u'itmf' in _genre:
            _genre_ref[u'itmf'] = _genre[u'itmf']
        return _genre_ref
    
    
    
    # Update nodes
    
    def update_tmdb_movie(self, tmdb_id):
        _movie = self.movies.find_one({u'tmdb_id':tmdb_id})
        url = repository_config['Database']['tmdb']['urls']['Movie.getInfo'].format(tmdb_id)
        handler = TmdbJsonHandler(url)
        element = handler.element()
        if element is not None:
            element = element[0]
            if _movie is None:
                _movie = {u'cast':[], u'genre':[], u'posters':[]}
                
            update_int_property(u'tmdb_id', element[u'id'], _movie)
            self.movies.save(_movie)
            update_int_property(u'imdb_id', element[u'imdb_id'], _movie)
            update_string_property(u'name', element[u'name'], _movie)
            update_string_property(u'overview', element[u'overview'], _movie)
            update_string_property(u'tagline', element[u'tagline'], _movie)
            update_string_property(u'content_rating', element[u'certification'], _movie)
            update_date_property(u'released', element[u'released'], _movie)
            
            if u'genres' in element.keys():
                _movie[u'genre'] = []
                for ge in element[u'genres']:
                    if ge[u'type'] == u'genre':
                        _movie[u'genre'].append(self._make_genre_item(ge[u'name']))
                        
            if u'cast' in element.keys():
                _movie[u'cast'] = []
                for ce in element[u'cast']:
                    _person_ref = self._make_person_ref_from_element(ce)
                    if _person_ref is not None:
                        _movie[u'cast'].append(_person_ref)
                                    
            if u'posters' in element.keys():
                _movie[u'posters'] = []
                posters = [ p['image'] for p in element[u'posters'] if p['image']['type'] == 'poster' and p['image']['size'] == 'original']
                if posters:
                    for p in posters:
                        _movie[u'posters'].append(p)
                    _movie[u'posters'][0]['selected'] = True
            
            _movie['last_update'] = datetime.utcnow()
            self.movies.save(_movie)
            self.logger.info(u'Creating Movie %s with IMDB ID %s', _movie[u'name'], _movie[u'imdb_id'])
        return _movie
    
    
    def update_tvdb_show_tree(self, tvdb_id):
        show = self.shows.find_one({u'tvdb_id':tvdb_id})
        if show is not None:
            url = repository_config['Database']['tvdb']['urls']['Show.getInfo'].format(tvdb_id)
            element = TvdbXmlHandler(url).element()
            show = self.update_tvdb_show(show, element)
            self.update_tvdb_episodes(show, element)
        else:
            self.logger.error(u'Show %d does not exist', tvdb_id)
        return show
    
    
    def update_tvdb_show(self, show, etree):
        show_nodes = etree.findall(u'Series')
        if show_nodes:
            show[u'genre'] = []
            show[u'cast'] = []
            for item in show_nodes[0].getchildren():
                if is_tag(u'IMDB_ID', item):
                    update_string_property(u'imdb_id', item.text, show)
                elif is_tag(u'lastupdated', item):
                    update_int_property(u'tvdb_last_update', int(item.text), show)
                elif is_tag(u'SeriesName', item):
                    update_string_property(u'name', item.text, show)
                elif is_tag(u'Overview', item):
                    update_string_property(u'overview', item.text, show)
                elif is_tag(u'ContentRating', item):
                    update_string_property(u'content_rating', item.text, show)
                elif is_tag(u'Network', item):
                    if item.text:
                        _network = self.find_network(item.text)
                        update_string_property(u'network_id', _network[u'_id'], show)
                        update_string_property(u'network', _network[u'name'], show)
                elif is_tag(u'Genre', item):
                    show[u'genre'] = []
                    genre_list = self._split_tvdb_list(item.text)
                    for g in genre_list:
                        show[u'genre'].append(self._make_genre_item(g))
                elif is_tag(u'Actors', item):
                    show[u'cast'] = []
                    actor_list = self._split_tvdb_list(item.text)
                    for actor in actor_list:
                        _person_ref = self._make_person_ref(job=u'actor', department=u'actors', person_name=actor)
                        if _person_ref is not None:
                            show[u'cast'].append(_person_ref)
                            
            show['last_update'] = datetime.utcnow()
            self.shows.save(show)
        return show
    
    
    def update_tvdb_episodes(self, show, etree):
        episode_nodes = etree.findall(u'Episode')
        if episode_nodes :
            for episode_item in episode_nodes:
                tvdb_episode_id = int(episode_item.find(u'id').text)
                episode = self.episodes.find_one({u'tvdb_id':tvdb_episode_id})
                if episode is None:
                    episode = {u'show':show[u'name'], u'show_small_name':show[u'small_name'], u'cast':[]}
                else:
                    episode[u'cast'] = []
                    
                for item in episode_item.getchildren():
                    if is_tag(u'id', item):
                        update_int_property(u'tvdb_id', int(item.text), episode)
                    elif is_tag(u'seriesid', item):
                        update_int_property(u'show_tvdb_id', int(item.text), episode)
                    elif is_tag(u'seasonid', item):
                        update_int_property(u'season_tvdb_id', int(item.text), episode)
                    elif is_tag(u'IMDB_ID', item):
                        update_string_property(u'imdb_id', item.text, episode)
                    elif is_tag(u'EpisodeName', item):
                        update_string_property(u'name', item.text, episode)
                    elif is_tag(u'EpisodeNumber', item):
                        update_int_property(u'episode_number', int(item.text), episode)
                    elif is_tag(u'SeasonNumber', item):
                        update_int_property(u'season_number', int(item.text), episode)
                    elif is_tag(u'Overview', item):
                        update_string_property(u'overview', item.text, episode)
                    elif is_tag(u'ProductionCode', item):
                        update_string_property(u'production_code', item.text, episode)
                    elif is_tag(u'FirstAired', item):
                        update_date_property(u'released', item.text, episode)
                    elif is_tag(u'filename', item):
                        update_string_property(u'poster', item.text, episode)
                    elif is_tag(u'Director', item):
                        director_list = self._split_tvdb_list(item.text)
                        for director in director_list:
                            _person_ref = self._make_person_ref(job=u'director', department=u'directing', person_name=director)
                            if _person_ref is not None:
                                episode[u'cast'].append(_person_ref)
                    elif is_tag(u'Writer', item):
                        writer_list = self._split_tvdb_list(item.text)
                        for writer in writer_list:
                            _person_ref = self._make_person_ref(job=u'screenplay', department=u'writing', person_name=writer)
                            if _person_ref is not None:
                                episode[u'cast'].append(_person_ref)
                    elif is_tag(u'GuestStars', item):
                        actor_list = self._split_tvdb_list(item.text)
                        for actor in actor_list:
                            _person_ref = self._make_person_ref(job=u'actor', department=u'actors', person_name=actor)
                            if _person_ref is not None:
                                episode[u'cast'].append(_person_ref)
                episode['last_update'] = datetime.utcnow()
                self.episodes.save(episode)
    
    
    
    def _find_tmdb_id_by_imdb_id(self, imdb_id):
        _tmdb_id = None
        url = repository_config['Database']['tmdb']['urls']['Movie.imdbLookup'].format(imdb_id)
        handler = TmdbJsonHandler(url)
        element = handler.element()
        if element is not None:
            element = element[0]
            _tmdb_id = element[u'id']
        return _tmdb_id
    
    
    def _find_person_by_name(self, name):
        name = collapse_whitespace.sub(u' ', name)
        name = name.strip()
        small_name = name.lower()
        _person = None
        if small_name is not None and len(small_name) > 0:
            _person = self.people.find_one({u'small_name':small_name})
            if _person is None:
                tmdb_person_id = self._find_tmdb_person_id_by_name(name)
                if tmdb_person_id is not None:
                    _person = self.find_person_by_tmdb_id(tmdb_person_id)
                else:
                    _person = self._make_person_stub(name)
        return _person
    
    
    def _make_person_stub(self, name):
        _person = {u'small_name':name.lower(), u'name':name}
        _person['last_update'] = datetime.utcnow()
        self.people.save(_person)
        return _person
    
    
    def update_tmdb_person(self, tmdb_id):
        _person = self.people.find_one({u'tmdb_id':tmdb_id})
        url = repository_config['Database']['tmdb']['urls']['Person.getInfo'].format(tmdb_id)
        handler = TmdbJsonHandler(url)
        element = handler.element()
        if element is not None:
            element = element[0]
            if _person is None:
                _person = {u'filmography':[]}
            update_int_property(u'tmdb_id', element[u'id'], _person)
            update_string_property(u'name', element[u'name'], _person)
            update_string_property(u'small_name', element[u'name'].lower(), _person)
            update_date_property(u'birthday', element[u'birthday'], _person)
            update_string_property(u'biography', element[u'biography'], _person)
            
            if u'filmography' in element.keys():
                _person[u'filmography'] = []
                for fe in element[u'filmography']:
                    _movie_ref = self._make_movie_ref_from_element(fe)
                    if _movie_ref is not None:
                        _person[u'filmography'].append(_movie_ref)
            _person['last_update'] = datetime.utcnow()
            self.people.save(_person)
        return _person
    
    
    def _find_tmdb_person_id_by_name(self, name):
        result = None
        n = collapse_whitespace.sub(u' ', name).lower()
        url = repository_config['Database']['tmdb']['urls']['Person.search'].format(format_tmdb_query(n))
        handler = TmdbJsonHandler(url)
        element = handler.element()
        if element is not None:
            for pe in element:
                if pe[u'name'].lower() == n:
                    result = pe[u'id']
                    self.logger.debug(u'Found a match: %s with tmdb id %d for %s', pe[u'name'], pe[u'id'], name)
                    break
                else:
                    self.logger.debug(u'Almost... %s with tmdb id %d does not match %s', pe[u'name'], pe[u'id'], name)
            
            if result is None:
                simple_name = remove_accents(n).strip()
                self.logger.debug(u'Trying to find a match for %s without accents', name)
                for pe in element:
                    if remove_accents(pe[u'name'].lower()) == simple_name:
                        result = pe[u'id']
                        self.logger.debug(u'Found a match: %s with tmdb id %d for %s', pe[u'name'], pe[u'id'], name)
                        break
                    else:
                        self.logger.debug(u'Almost... %s with tmdb id %d does not match %s', pe[u'name'], pe[u'id'], name)
        return result
    
    
    def _make_person_ref_from_element(self, element):
        return self._make_person_ref(element[u'job'], element[u'department'], element[u'character'], element[u'id'], element[u'name'])
    
    
    def _make_person_ref(self, job, department, character=None, person_tmdb_id=None, person_name=None):
        _person_ref = None
        _person = None
        _department = self.find_department(department)
        _job = self.find_job(job)
        if person_tmdb_id is not None:
            _person = self.find_person_by_tmdb_id(person_tmdb_id)
        
        if _person is None:
            _person = self._find_person_by_name(person_name)
            
        if _person is not None:
            _person_ref = {}
            _person_ref[u'id'] = _person[u'_id']
            if u'tmdb_id' in _person:
                update_int_property(u'tmdb_id', _person[u'tmdb_id'], _person_ref)
            update_string_property(u'name', _person[u'name'], _person_ref)
            update_string_property(u'character', character, _person_ref)
            update_string_property(u'department', _department[u'_id'], _person_ref)
            update_string_property(u'job', _job[u'_id'], _person_ref)
        return _person_ref
    
    
    def _make_movie_ref_from_element(self, element):
        return self._make_movie_ref(element[u'job'], element[u'department'], element[u'id'], element[u'name'], element[u'character'])
    
    
    def _make_movie_ref(self, job, department, movie_tmdb_id, movie_name, character=None):
        _movie_ref = None
        _department = self.find_department(department)
        _job = self.find_job(job)
        
        if movie_tmdb_id is not None and movie_name is not None:
            _movie_ref = {}
            update_string_property(u'name', movie_name, _movie_ref)
            update_int_property(u'id', movie_tmdb_id, _movie_ref)
            update_string_property(u'job', _job[u'_id'], _movie_ref)
            update_string_property(u'department', _department[u'_id'], _movie_ref)
            update_string_property(u'character', character, _movie_ref)
        return _movie_ref
    
    
    def _split_tvdb_list(self, value):
        result = []
        if value is not None:
            value = tvdb_list_seperators.sub(u'|', value)
            value = strip_space_around_seperator.sub(u'|', value)
            value = value.strip().strip(u'|')
            if value:
                person_list = value.split(u'|')
                for p in person_list:
                    cp = clean_tvdb_person_name(p)
                    if cp is not None:
                        result.append(cp)
                    else:
                        self.logger.info(u'Ignoring weird person name %s', p)
        return result
    



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
        if value is None:
            del entity[key]
        else:
            entity[key] = value
    return result


def update_string_property(key, value, entity):
    result = False
    old_value = None
    if key in entity:
        old_value = entity[key]
        
    if value is not None:
        value = value.strip()
        if not len(value) > 0:
            value = None
            
    if old_value != value:
        result = True
        if value is None:
            del entity[key]
        else:
            entity[key] = value
    return result


def update_date_property(key, value, entity):
    result = False
    old_value = None
    if key in entity:
        old_value = entity[key]
        
    if value is not None:
        value = value.strip()
        if value and valid_tmdb_date.search(value) is not None:
            value = datetime.strptime(value, '%Y-%m-%d')
        else:
            value = None
            
    if old_value != value:
        result = True
        if value is None:
            del entity[key]
        else:
            entity[key] = value
    return result


def clean_tvdb_person_name(value):
    result = None
    if value is not None:
        value = tvdb_person_name_junk.sub(u'', value)
        value = value.strip()
        if len(value) < minimum_person_name_length:
            value = None
    return value
    


def format_tmdb_query(value):
    result = None
    if value is not None:
        value = collapse_whitespace.sub(u'+', value)
    return value


def remove_accents(value):
    nkfd_form = unicodedata.normalize('NFKD', value)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])



# Singletone
theEntityManager = EntityManager()

numberic_key_string_pair = re.compile(u'^([0-9]+):(.+)$', re.UNICODE)
minimum_person_name_length = repository_config['Database']['tvdb']['fuzzy']['minimum_person_name_length']
valid_tmdb_date = re.compile(u'[0-9]{4}-[0-9]{2}-[0-9]{2}', re.UNICODE)
tvdb_list_seperators = re.compile(ur'\||,', re.UNICODE)
strip_space_around_seperator = re.compile(ur'\s*\|\s*', re.UNICODE)
collapse_whitespace = re.compile(ur'\s+', re.UNICODE)
url_to_cache = re.compile(ur'http://', re.UNICODE)
image_http_type = re.compile(ur'image/.*', re.UNICODE)
tvdb_person_name_junk = re.compile(ur'\([^\)]+(?:\)|$)', re.UNICODE)