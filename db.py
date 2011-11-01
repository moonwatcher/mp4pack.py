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

class EntityManager(object):
    def __init__(self, configuration):
        self.logger = logging.getLogger('Entity Manager')
        self.configuration = configuration
        
        mongodb_conf = self.configuration.get_mongodb_config()
        self.logger.debug('Connecting to %s', mongodb_conf['url'])
        self.connection = pymongo.Connection(mongodb_conf['url'])
        self.db = self.connection[mongodb_conf['database']]
        self.sync_delay = self.configuration.user_config['horizon time delta']
        
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
        self.create_index()
        self.refresh_itmf_genres()
        self.refresh_tmdb_genres()
        
        # from config import base_config
        # for s in base_config['tvshow']:
        #    self.map_show(s[1], s[0])
    
    
    def list_all_movie_imdbs(self):
        return self.movies.find({}, {'imdb_id':1, 'tmdb_id':1})
    
    
    def list_all_tv_show_episode_ids(self):
        return self.episodes.find({}, {'_id':1})
    
    
    def create_index(self):
        self.genres.create_index(u'small_name', unique=True)
        self.departments.create_index(u'small_name', unique=True)
        self.jobs.create_index(u'small_name', unique=True)
        self.networks.create_index(u'small_name', unique=True)
        
        self.movies.create_index(u'imdb_id')
        self.movies.create_index(u'tmdb_id')
        self.movies.create_index(u'small_name')
        self.movies.create_index(u'simple_name')
        
        self.people.create_index(u'tmdb_id')
        self.people.create_index(u'small_name')
        self.people.create_index(u'simple_name')
        
        self.shows.create_index(u'tv_show_key')
        self.shows.create_index(u'tvdb_id')
        self.shows.create_index(u'small_name')
        self.shows.create_index(u'simple_name')
        
        self.episodes.create_index(
            [
                (u'tv_show_key', pymongo.DESCENDING),
                (u'tv_season', pymongo.DESCENDING),
                (u'tv_episode', pymongo.DESCENDING)
            ], unique=True
        )
        self.logger.info(u'Created mongodb indexes')
    
    
    def suppress_sync(self, sync, last_update):
        if sync:
            delta = datetime.utcnow() - last_update
            if delta < self.sync_delay:
                self.logger.debug(u'Supressing online sync. Next update possible in %s', unicode(self.sync_delay - delta))
                sync = False
            else:
                self.logger.info(u'Sync allowed. Fast forward %s', unicode(delta))
        return sync
    
    
    def refresh_tmdb_genres(self):
        url = self.configuration.service['tmdb']['urls']['Genres.getList']
        handler = TmdbJsonHandler(self, url)
        handler.refresh()
        element_list = handler.element()
        if element_list is not None:
            count = 0
            for element in element_list:
                if u'name' in element:
                    count += 1
                    self.store_tmdb_genre(element[u'name'], element[u'id'], element[u'url'])
            
            self.logger.info(u'Refreshed %s genres from tmdb', count)
        else:
            self.logger.warning(u'Could not get tmdb genres list', count)
    
    
    def refresh_itmf_genres(self):
        count = 0
        for genre in self.configuration.media_config['gnre']:
            count += 1
            self.store_itmf_genre(genre['print'], genre['code'])
        self.logger.info(u'Refreshed %s iTMF genres', count)
    
    
    def map_show_with_pair(self, pair):
        if pair is not None:
            match = numberic_key_string_pair.search(pair)
            if match is not None:
                self.map_show(unicode(match.group(2)), int(match.group(1)))
            else:
                self.logger.error(u'Could not parse %s', pair)
    
    
    def map_show(self, name, tvdb_id):
        tv_show_key = remove_accents(make_small_name(name))
        tvdb_id = int(tvdb_id)
        
        show_by_tvdb_id = self.shows.find_one({u'tvdb_id':tvdb_id})
        show_by_key = self.shows.find_one({u'tv_show_key':tv_show_key})
        if show_by_key is None and show_by_tvdb_id is None:
            # This is good, we can do the mapping
            show = {u'tv_show_key':tv_show_key, u'tvdb_id':tvdb_id, u'last_update':None}
            self.shows.save(show)
            self.logger.info(u'TV Show %s is now mapped to tvdb %d', tv_show_key, tvdb_id)
        else: # This means at least one exists
            if show_by_key is not None and show_by_tvdb_id is not None and show_by_tvdb_id[u'_id'] == show_by_key[u'_id']:
                # Both exist and are identical, so no mapping is needed
                self.logger.debug(u'TV Show %s to tvdb %d mapping exists', tv_show_key, tvdb_id)
            else:
                # Mapping is impossible. Either one or both exist and mapped to somethign else
                if show_by_key is not None:
                    self.logger.error(u'Show %s is already mapped to tvdb %d', show_by_key[u'tv_show_key'], show_by_key[u'tvdb_id'])
                if show_by_tvdb_id is not None:
                    self.logger.error(u'Show %s is already mapped to tvdb %d', show_by_tvdb_id[u'tv_show_key'], show_by_tvdb_id[u'tvdb_id'])
    
    
    def store_network(self, name):
        small_name = make_small_name(name)
        network = self.networks.find_one({u'small_name': small_name})
        if network is None:
            network = {u'small_name':small_name, u'name':name}
            self.networks.save(network)
            self.logger.info(u'Created TV Network %s', name)
        return network
    
    
    def store_job(self, name):
        small_name = make_small_name(name)
        job = self.jobs.find_one({u'small_name': small_name})
        if job is None:
            job = {u'small_name':small_name, u'name':name}
            self.jobs.save(job)
            self.logger.info(u'Created Job %s', name)
        return job
    
    
    def store_department(self, name):
        small_name = make_small_name(name)
        department = self.departments.find_one({u'small_name': small_name})
        if department is None:
            department = {u'small_name':small_name, u'name':name}
            self.departments.save(department)
            self.logger.info(u'Created Department %s', name)
        return department
    
    
    def map_genre(self, name, reference):
        small_reference_name = make_small_name(reference)
        reference_genre = self.genres.find_one({u'small_name':small_reference_name})
        if reference_genre is not None:
            small_name = make_small_name(name)
            genre = self.genres.find_one({u'small_name':small_name})
            if genre is None:
                # mapped genre does not exist
                genre = {u'small_name':small_name, u'name':name, u'reference':small_reference_name}
                self.genres.save(genre)
                self.logger.info(u'Mapping new genre %s to %s', name, reference)
            elif u'itmf' in genre:
                # mapped genre is an itmf genre, refuse mapping
                self.logger.error(u'Refusing to map itmf genre %s to %s', name, reference)
            elif u'tmdb_id' in genre:
                # mapped genre is tmdb genre, refuse mapping
                self.logger.error(u'Refusing to map tmdb genre %s to %s', name, reference)
            else:
                # mapped genre exists
                genre[u'reference':small_reference_name]
                self.genres.save(genre)
                self.logger.info(u'Mapping existing genre %s to %s', name, reference)
        else:
            self.logger.error(u'Can not map % to non existing genre %s', name, reference)
        return genre
    
    
    def store_tmdb_genre(self, name, tmdb_id, url):
        small_name = make_small_name(name)
        genre = self.genres.find_one({u'small_name':small_name})
        if genre is None:
            genre = {u'small_name':small_name, u'name':name, u'tmdb_id':tmdb_id, u'url':url}
            self.logger.info(u'Created genre %s with tmdb %s', genre[u'name'], genre[u'tmdb_id'])
        elif u'tmdb_id' not in genre:
            genre[u'tmdb_id'] = tmdb_id
            genre[u'url'] = url
            self.logger.info(u'Added tmdb id %s to genre %s', genre[u'tmdb_id'], genre[u'name'])
        self.genres.save(genre)
        return genre
    
    
    def store_itmf_genre(self, name, itmf):
        small_name = make_small_name(name)
        genre = self.genres.find_one({u'small_name':small_name})
        if genre is None:
            genre = {u'small_name':small_name, u'name':name, u'itmf':itmf}
            self.genres.save(genre)
            self.logger.info(u'Created genre %s with itmf %s', genre[u'name'], genre[u'itmf'])
        elif u'itmf' not in genre:
            genre[u'itmf'] = itmf
            self.logger.info(u'Added itmf code %s to genre %s', genre[u'itmf'], genre[u'name'])
        return genre
    
    
    def store_genre(self, name):
        small_name = make_small_name(name)
        genre = self.genres.find_one({u'small_name':small_name})
        if genre is None:
            genre = {u'small_name':small_name, u'name':name}
            self.genres.save(genre)
            self.logger.info(u'Created genre %s', genre[u'name'])
        return genre
    
    
    
    def save_tv_show(self, show):
        if show:
            self.shows.save(show)
    
    
    def save_tv_episode(self, tv_episode):
        if tv_episode:
            self.episodes.save(tv_episode)
    
    
    def save_movie(self, movie):
        if movie:
            self.movies.save(movie)
    
    
    def find_movie_by_imdb_id(self, imdb_id, refresh=False):
        movie = self.movies.find_one({u'imdb_id': imdb_id})
        if movie is None:
            tmdb_id = self.find_tmdb_movie_id_by_imdb_id(imdb_id)
            if tmdb_id is not None:
                movie = self.find_movie_by_tmdb_id(tmdb_id, refresh)
        elif refresh and u'tmdb_id' in movie:
            movie = self.find_movie_by_tmdb_id(movie[u'tmdb_id'], refresh)
        return movie
    
    
    def find_movie_by_tmdb_id(self, tmdb_id, refresh=False):
        tmdb_id = int(tmdb_id)
        movie = self.movies.find_one({u'tmdb_id':tmdb_id})
        if movie is None or self.suppress_sync(refresh, movie['last_update']):
            movie = self.store_tmdb_movie(tmdb_id, refresh)
        return movie
    
    
    def find_person_by_tmdb_id(self, tmdb_id, refresh=False):
        tmdb_id = int(tmdb_id)
        person = self.people.find_one({u'tmdb_id':tmdb_id})
        if person is None or self.suppress_sync(refresh, person['last_update']):
            person = self.store_tmdb_person(tmdb_id, refresh)
        return person
    
    
    def find_show(self, tv_show_key, refresh=False):
        show = self.shows.find_one({u'tv_show_key': tv_show_key})
        if show is not None and u'tvdb_id' in show:
            if show[u'last_update'] is None or self.suppress_sync(refresh, show['last_update']):
                self.logger.info(u'Updating show %s', tv_show_key)
                show, episodes = self.store_tvdb_show(show[u'tvdb_id'], refresh)
                self.logger.info(u'Done updating show %s', tv_show_key)
        else:
            self.logger.error(u'Show %s does not exist', tv_show_key)
        return show
    
    
    def find_episode_by_id(self, id):
        return self.episodes.find_one({'_id':id})
    
    
    def find_episode(self, tv_show_key, tv_season, tv_episode, refresh=False):
        show = self.find_show(tv_show_key, refresh)
        episode = None
        if show is not None:
            episode = self.episodes.find_one({u'tv_show_key':tv_show_key, u'tv_season':tv_season, u'tv_episode':tv_episode})
            #if episode is None:
            #    self.logger.info(u'Could not find episode, updating show %s', tv_show_small_name)
            #    self.store_tvdb_show(show[u'tvdb_id'], refresh)
            #    self.logger.info(u'Done updating show %s', tv_show_small_name)
            #    episode = self.episodes.find_one({u'tv_show_small_name':tv_show_small_name, u'tv_season':tv_season, u'tv_episode':tv_episode})
        return show, episode
    
    
    def choose_tmdb_movie_poster_with_pair(self, pair, refresh=False):
        if pair is not None:
            match = string_key_string_pair.search(pair)
            if match is not None:
                self.choose_tmdb_movie_poster(match.group(1), match.group(2), refresh)
            else:
                self.logger.error(u'Could not parse %s', pair)
    
    
    def choose_tmdb_movie_poster(self, imdb_id, tmdb_poster_id, refresh=False):
        movie = self.find_movie_by_imdb_id(imdb_id)
        poster = None
        if movie is not None and u'tmdb_record' in movie:
            posters = [ p for p in movie[u'tmdb_record'][u'posters'] if p['image']['size'] == 'original' ]
            if tmdb_poster_id:
                posters = [ p for p in posters if p['image']['id'] == tmdb_poster_id ]
            if posters:
                poster = posters[0]
                movie['poster'] = poster['image']['id']
                self.movies.save(movie)
                if refresh:
                    handler = ImageHandler(self, poster['image']['url'])
                    handler.refresh()
                self.logger.info(u'Poster %s selected for movie %s imdb:%s', movie['poster'], movie['name'], imdb_id)
            else:
                self.logger.error(u'No poster with id %s found for movie %s imdb:%s', tmdb_poster_id, movie['name'], imdb_id)
        else:
            self.logger.error(u'No movie with imdb id %s found', imdb_id)
        return poster
    
    
    def find_tmdb_movie_poster(self, imdb_id):
        poster = None
        movie = self.find_movie_by_imdb_id(imdb_id)
        if movie is not None and u'tmdb_record' in movie and movie[u'poster']:
            posters = [ p for p in movie[u'tmdb_record'][u'posters'] if p['image']['size'] == 'original' and p['image']['id'] == movie['poster'] ]
            if posters:
                poster = posters[0]
                handler = ImageHandler(self, poster['image']['url'])
                if handler.cache():
                    poster['cache'] = {'path':handler.local(), 'kind':os.path.splitext(handler.local())[1].strip('.')}
        return poster
    
    
    def find_tvdb_episode_poster(self, tv_show_key, tv_season, tv_episode):
        poster = None
        show, episode = self.find_episode(tv_show_key, tv_season, tv_episode)
        if episode is not None and 'tvdb_record' in episode:
            if episode['tvdb_record']['posters']:
                poster = episode['tvdb_record']['posters'][0]
                handler = TvdbImageHandler(self, poster['image']['url'])
                if handler.cache():
                    poster['cache'] = {'path':handler.local(), 'kind':os.path.splitext(handler.local())[1].strip('.')}
        return poster
    
    
    
    def store_tmdb_person(self, tmdb_id, refresh=False):
        tmdb_id = int(tmdb_id)
        new_record = False
        person = self.people.find_one({u'tmdb_id':tmdb_id})
        url = self.configuration.service['tmdb']['urls']['Person.getInfo'].format(tmdb_id)
        handler = TmdbJsonHandler(self, url)
        if refresh: handler.refresh()
        element = handler.element()
        if element is not None:
            element = element[0]
            if person is None:
                person = { 'tmdb_id':tmdb_id }
                new_record = True
            person['name'] = element['name'].strip()
            person['small_name'] = make_small_name(person['name'])
            person['simple_name'] = remove_accents(person['small_name'])
            person['last_update'] = datetime.utcnow()
            person['tmdb_record'] = element
            self.people.save(person)
            
            if new_record:
                self.logger.info(u'Created record for person %s with tmdb %s', person['tmdb_record']['name'], person['tmdb_id'])
            else:
                self.logger.info(u'Updated record for person %s with tmdb %s', person['tmdb_record']['name'], person['tmdb_id'])
        return person
    
    
    def store_tmdb_movie(self, tmdb_id, refresh=False):
        tmdb_id = int(tmdb_id)
        new_record = False
        movie = self.movies.find_one({u'tmdb_id':tmdb_id})
        url = self.configuration.service['tmdb']['urls']['Movie.getInfo'].format(tmdb_id)
        handler = TmdbJsonHandler(self, url)
        if refresh: handler.refresh()
        element = handler.element()
        if element is not None:
            element = element[0]
            if movie is None:
                movie = { 'tmdb_id':tmdb_id, 'poster':None }
                new_record = True
            movie['imdb_id'] = element['imdb_id']
            movie['name'] = element['name']
            movie['small_name'] = make_small_name(element['name'])
            movie['simple_name'] = remove_accents(movie['small_name'])
            movie['last_update'] = datetime.utcnow()
            movie['tmdb_record'] = element
            
            posters = [ p for p in movie[u'tmdb_record'][u'posters'] if p['image']['size'] == 'original' ]
            if movie['poster']:
                if posters:
                     selected = [ p for p in posters if p['image']['id'] == movie['poster'] ]
                     if not selected:
                         movie['poster'] = posters[0]['image']['id']
                else:
                    movie['poster'] = None
                    self.logger.warning(u'No poster found for %s imdb:%s', movie['name'], movie['imdb_id'])
            elif posters:
                movie['poster'] = posters[0]['image']['id']
                
            self.movies.save(movie)
            
            if 'cast' in element.keys():
                for person in element['cast']:
                    self.find_person_by_tmdb_id(person['id'], refresh)
            if new_record:
                self.logger.info(u'Created record for movie %s with tmdb:%s imdb:%s', movie['tmdb_record']['name'], movie['tmdb_id'], movie['imdb_id'])
            else:
                self.logger.info(u'Updated record for movie %s with tmdb:%s imdb:%s', movie['tmdb_record']['name'], movie['tmdb_id'], movie['imdb_id'])
        return movie
    
    
    def find_tmdb_movie_id_by_imdb_id(self, imdb_id):
        tmdb_id = None
        url = self.configuration.service['tmdb']['urls']['Movie.imdbLookup'].format(imdb_id)
        handler = TmdbJsonHandler(self, url)
        element = handler.element()
        if element is not None:
            element = element[0]
            tmdb_id = element['id']
        return tmdb_id
    
    
    def find_genre_by_name(self, name):
        genre = self.store_genre(name)
        while genre and 'reference' in genre:
            genre = self.genres.find_one({u'small_name':genre['reference']})
        return genre
    
    
    def find_person_by_name(self, name, refresh=False):
        person = None
        name = collapse_whitespace.sub(u' ', name).strip()
        small_name = make_small_name(name)
        if small_name:
            person = self.people.find_one({'small_name':small_name})
            if person is None:
                simple_name = remove_accents(small_name)
                person = self.people.find_one({'simple_name':simple_name})
        
        if person and 'tmdb_id' in person:
            person = self.find_person_by_tmdb_id(person['tmdb_id'], refresh)
        else:
            if person is None:
                tmdb_id = self.find_tmdb_person_id_by_name(name)
                if tmdb_id:
                    person = self.find_person_by_tmdb_id(tmdb_id, refresh)
                else:
                    person = self.make_person_stub(name)
            elif self.suppress_sync(refresh, person['last_update']):
                tmdb_id = self.find_tmdb_person_id_by_name(name)
                if tmdb_id:
                    # Person was a stub, update tmdb id and refresh
                    person['tmdb_id'] = tmdb_id
                    self.people.save(person)
                    self.logger.info('Updated existing stub person record for %s with new tmdb id %d', name, tmdb_id)
                    person = self.find_person_by_tmdb_id(tmdb_id, True)
        return person
    
    
    def find_tmdb_person_id_by_name(self, name):
        person = None
        clean = collapse_whitespace.sub(u' ', name).lower()
        url = self.configuration.service['tmdb']['urls']['Person.search'].format(format_tmdb_query(clean))
        handler = TmdbJsonHandler(self, url)
        element = handler.element()
        if element is not None:
            for potential in element:
                if potential['name'].lower() == clean:
                    person = potential['id']
                    self.logger.debug(u'Found a match: %s with tmdb %d for %s', potential['name'], potential['id'], name)
                    break
                else:
                    self.logger.debug(u'Not a match: %s with tmdb %d for %s', potential['name'], potential['id'], name)
            if person is None:
                self.logger.debug(u'Trying to match %s without accents', name)
                simple_name = remove_accents(clean)
                for potential in element:
                    if remove_accents(potential['name'].lower()) == simple_name:
                        person = potential['id']
                        self.logger.debug(u'Found a match: %s with tmdb id %d for %s', potential['name'], potential['id'], name)
                        break
                    else:
                        self.logger.debug(u'Not a match: %s with tmdb id %d for %s', potential['name'], potential['id'], name)
        return person
    
    
    def make_person_stub(self, name):
        person = {
            'name':name.strip(),
            'small_name':make_small_name(name)
        }
        person['last_update'] = datetime.utcnow()
        self.people.save(person)
        return person
    
    
    def make_person_reference(self, person):
        reference = None
        if person:
            reference = {}
            if 'tmdb_record' in person:
                reference['name'] = person['tmdb_record']['name']
                reference['id'] = person['tmdb_record']['id']
                if 'url' in person['tmdb_record']:
                    reference['url'] = person['tmdb_record']['url']
                
                if 'profile' in person['tmdb_record']:
                    thumbs = [ 
                        v['image']['url'] for v in person['tmdb_record']['profile'] 
                        if v['image']['size'] == 'thumb' 
                        and v['image']['type'] == 'profile'
                    ]
                    if thumbs:
                        reference['profile'] = thumbs[0]
            else:
                # Person has no tmdb record
                reference['name'] = person['name']
        return reference
    
    
    def make_genre_reference(self, genre):
        reference = None
        if genre:
            reference = {'type':'genre', 'name':genre['name']}
            if 'itmf' in genre:
                reference['itmf'] = genre['itmf']
            if 'tmdb_id' in genre:
                reference['id'] = genre['tmdb_id']
                reference['url'] = genre['url']
        return reference
    
    
    def store_tvdb_show(self, tvdb_id, refresh=False):
        tvdb_id = int(tvdb_id)
        show = self.shows.find_one({'tvdb_id':tvdb_id})
        if show is not None:
            url = self.configuration.service['tvdb']['urls']['Show.getInfo'].format(tvdb_id)
            handler = TvdbXmlHandler(self, url)
            if refresh: handler.refresh()
            element = handler.element()
            
            # store information about the show
            node = element.findall('Series')
            if node and node[0]:
                node = node[0]
                show['tvdb_record'] = {'cast':[], 'genres':[], 'posters':[]}
                for item in node.getchildren():
                    if item.tag == 'IMDB_ID':
                        update_string_property(u'imdb_id', item.text, show['tvdb_record'])
                    elif item.tag == 'lastupdated':
                        update_timestamp_property('last_modified_at', item.text, show['tvdb_record'])
                    elif item.tag == 'SeriesName':
                        update_string_property(u'name', item.text, show['tvdb_record'])
                    elif item.tag == 'Overview':
                        update_string_property(u'overview', item.text, show['tvdb_record'])
                    elif item.tag == 'ContentRating':
                        update_string_property(u'certification', item.text, show['tvdb_record'])
                    elif item.tag == 'FirstAired':
                        update_date_property(u'first_aired', item.text, show['tvdb_record'])
                    elif item.tag == 'Language':
                        update_string_property(u'language', item.text, show['tvdb_record'])
                    elif item.tag == 'Rating':
                        update_float_property(u'rating', item.text, show['tvdb_record'])
                    elif item.tag == 'RatingCount':
                        update_int_property(u'votes', item.text, show['tvdb_record'])
                    elif item.tag == 'Runtime':
                        update_int_property(u'runtime', item.text, show['tvdb_record'])
                    elif item.tag == 'poster':
                        if item.text:
                            show['tvdb_record']['posters'].append({'image':{'type':'poster', 'size':'original', 'url':item.text.strip()}})
                    elif item.tag == 'Network':
                        if item.text:
                            network = self.store_network(item.text)
                            update_string_property(u'tv_network', network['name'], show['tvdb_record'])
                    elif item.tag == 'Genre':
                        genre_names = self.split_tvdb_list(item.text)
                        if genre_names:
                            for genre_name in genre_names:
                                genre = self.find_genre_by_name(genre_name)
                                if genre:
                                    reference = self.make_genre_reference(genre)
                                    show['tvdb_record'][u'genres'].append(reference)
                    elif item.tag  == 'Actors':
                        people_names = self.split_tvdb_list(item.text)
                        if people_names:
                            for person_name in people_names:
                                person = self.find_person_by_name(person_name, refresh)
                                if person:
                                    reference = self.make_person_reference(person)
                                    if reference:
                                        reference['job'] = 'Actor'
                                        reference['department'] = 'Actors'
                                        show['tvdb_record']['cast'].append(reference)
                show['last_update'] = datetime.utcnow()
                update_string_property(u'name', show['tvdb_record']['name'], show)
                update_string_property(u'small_name', make_small_name(show['name']), show)
                update_string_property(u'simple_name', remove_accents(show['small_name']), show)
                self.shows.save(show)
                self.logger.info(u'Updated record for TV show %s with tvdb %s', show[u'small_name'], show[u'tvdb_id'])
            
            # Now go through the episodes
            node = element.findall('Episode')
            if node:
                episodes = []
                for episode in node:
                    e = self.store_tvdb_episode(show, episode, refresh)
                    if e: episodes.append(e)
        else:
            self.logger.error(u'Show %d does not exist', tvdb_id)
        return show, episodes
    
    
    def store_tvdb_episode(self, show, node, refresh=False):
        episode = None
        if node:
            tv_season = int(node.find('SeasonNumber').text)
            if tv_season > 0:
                tv_episode = int(node.find('EpisodeNumber').text)
                tv_episode_name = node.find('EpisodeName').text
                if tv_episode_name: tv_episode_name = tv_episode_name.strip()
                
                if tv_episode and tv_episode > 0 and tv_episode_name:
                    episode = self.episodes.find_one({u'tv_show_key':show['tv_show_key'], 'tv_season':tv_season, 'tv_episode':tv_episode})
                    if episode is None:
                        episode = {
                            'tv_show_key':show['tv_show_key'],
                            'tvdb_show_id':show['tvdb_id'],
                            'tv_season':tv_season,
                            'tv_episode':tv_episode
                        }
                    update_string_property(u'name', tv_episode_name, episode)
                    update_string_property(u'small_name', make_small_name(episode['name']), episode)
                    update_string_property(u'simple_name', remove_accents(episode['small_name']), episode)
                    episode['tvdb_record'] = {'cast':[], 'posters':[]}
                    for item in node.getchildren():
                        if item.tag == 'IMDB_ID':
                            update_string_property(u'imdb_id', item.text, episode['tvdb_record'])
                        elif item.tag == 'lastupdated':
                            update_timestamp_property('last_modified_at', item.text, episode['tvdb_record'])
                        if item.tag == 'id':
                            update_int_property('tvdb_id', item.text, episode['tvdb_record'])
                        elif item.tag == 'seriesid':
                            update_int_property(u'tvdb_show_id', item.text, episode['tvdb_record'])
                        elif item.tag == 'seasonid':
                            update_int_property(u'tvdb_season_id', item.text, episode['tvdb_record'])
                        elif item.tag == 'EpisodeName':
                            update_string_property(u'name', item.text, episode['tvdb_record'])
                        elif item.tag == 'EpisodeNumber':
                            update_int_property(u'tv_episode', item.text, episode['tvdb_record'])
                        elif item.tag == 'SeasonNumber':
                            update_int_property(u'tv_season', item.text, episode['tvdb_record'])
                        elif item.tag == 'absolute_number':
                            update_int_property(u'absolute_tv_episode', item.text, episode['tvdb_record'])
                        elif item.tag == 'Overview':
                            update_string_property(u'overview', item.text, episode['tvdb_record'])
                        elif item.tag == 'ProductionCode':
                            update_string_property(u'production_code', item.text, episode['tvdb_record'])
                        elif item.tag == 'FirstAired':
                            update_date_property(u'released', item.text, episode['tvdb_record'])
                        elif item.tag == 'Rating':
                            update_float_property(u'rating', item.text, episode['tvdb_record'])
                        elif item.tag == 'RatingCount':
                            update_int_property(u'votes', item.text, episode['tvdb_record'])
                        elif item.tag == 'filename':
                            if item.text:
                                episode['tvdb_record']['posters'].append({'image':{'type':'poster', 'size':'cover', 'url':item.text.strip()}})
                        elif item.tag == 'Director':
                            people_names = self.split_tvdb_list(item.text)
                            if people_names:
                                for person_name in people_names:
                                    person = self.find_person_by_name(person_name, refresh)
                                    if person:
                                        reference = self.make_person_reference(person)
                                        if reference:
                                            reference['job'] = 'Director'
                                            reference['department'] = 'Directing'
                                            episode['tvdb_record']['cast'].append(reference)
                        elif item.tag == 'Writer':
                            people_names = self.split_tvdb_list(item.text)
                            if people_names:
                                for person_name in people_names:
                                    person = self.find_person_by_name(person_name, refresh)
                                    if person:
                                        reference = self.make_person_reference(person)
                                        if reference:
                                            reference['job'] = 'Screenplay'
                                            reference['department'] = 'Writing'
                                            episode['tvdb_record']['cast'].append(reference)
                        elif item.tag == 'GuestStars':
                            people_names = self.split_tvdb_list(item.text)
                            if people_names:
                                for person_name in people_names:
                                    person = self.find_person_by_name(person_name, refresh)
                                    if person:
                                        reference = self.make_person_reference(person)
                                        if reference:
                                            reference['job'] = 'Actor'
                                            reference['department'] = 'Actors'
                                            episode['tvdb_record']['cast'].append(reference)
                    episode['last_update'] = datetime.utcnow()
                    self.episodes.save(episode)
                    self.logger.info(u'Updated record for TV Show %s season %d episode %d: %s', 
                        show[u'name'],
                        episode[u'tv_season'],
                        episode[u'tv_episode'],
                        episode[u'name']
                    )
                else:
                    self.logger.warning(u'Ignoring bogus episode for TV Show %s season %d episode %d: %s', 
                        show[u'name'],
                        tv_season,
                        tv_episode,
                        tv_episode_name
                    )
            else:
                self.logger.debug(u'Ignoring episode for TV Show %s with non positive season', show['tvdb_record']['name'])
        return episode
    
    
    def split_tvdb_list(self, value):
        result = []
        if value is not None:
            value = tvdb_list_seperators.sub(u'|', value)
            value = strip_space_around_seperator.sub(u'|', value)
            value = value.strip().strip(u'|')
            if value:
                person_list = value.split(u'|')
                for p in person_list:
                    cp = self.clean_tvdb_person_name(p)
                    if cp is not None:
                        result.append(cp)
                    else:
                        self.logger.debug(u'Dropping bogus name %s', p)
        return result
    
    
    def clean_tvdb_person_name(self, value):
        result = None
        if value is not None:
            value = self.tvdb_person_name_junk.sub(u'', value)
            value = value.strip()
            if len(value) < self.configuration.service['tvdb']['fuzzy']['minimum_person_name_length']:
                value = None
        return value
    
    
    tvdb_person_name_junk = re.compile(ur'\([^\)]+(?:\)|$)', re.UNICODE)



class ResourceHandler(object):
    def __init__(self, entity_manager, url):
        self.logger = logging.getLogger('Resource Handler')
        self.entity_manager = entity_manager
        self.remote_url = url
        self.local_path = self.local()
        self.headers = None
    
    
    def local(self):
        return url_to_cache.sub(self.entity_manager.configuration.get_cache_path(), self.remote_url)
    
    
    def cache(self):
        result = True
        if not os.path.exists(self.local_path):
            dirname = os.path.dirname(self.local_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            try:
                self.logger.debug(u'Retrieve %s', self.remote_url)
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
    
    
    def refresh(self):
        self.clean()
        self.cache()
    
    


class JsonHandler(ResourceHandler):
    def __init__(self, entity_manager, url):
        ResourceHandler.__init__(self, entity_manager, url)
        self.logger = logging.getLogger('Json Handler')
    
    
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
    def __init__(self, entity_manager, url):
        ResourceHandler.__init__(self, entity_manager, url)
        self.logger = logging.getLogger('Image Handler')
    
    
    def cache(self):
        result = ResourceHandler.cache(self)
        if self.headers is not None and image_http_type.search(self.headers.type) is None:
            self.clean()
            result = False
        return result
    
    


class XmlHandler(ResourceHandler):
    def __init__(self, entity_manager, url):
        ResourceHandler.__init__(self, entity_manager, url)
        self.logger = logging.getLogger('Xml Handler')
    
    
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
    def __init__(self, entity_manager, url):
        JsonHandler.__init__(self, entity_manager, url)
        self.logger = logging.getLogger('Tmdb Json Handler')
    
    
    def local(self):
        result = ResourceHandler.local(self)
        result = result.replace(u'/{0}'.format(self.entity_manager.configuration.service['tmdb']['apikey']), u'')
        return result
    
    
    def element(self):
        element = JsonHandler.element(self)
        if not element or element[0] == u'Nothing found.':
            element = None
            self.clean()
            self.logger.debug(u'Nothing found in %s', self.remote_url)
        return element
    
    


class TvdbXmlHandler(XmlHandler):
    def __init__(self, entity_manager, url):
        XmlHandler.__init__(self, entity_manager, url)
        self.logger = logging.getLogger('Tvdb Xml Handler')
    
    
    def local(self):
        result = ResourceHandler.local(self)
        result = result.replace(u'/{0}'.format(self.entity_manager.configuration.service['tvdb']['apikey']), u'')
        result = result.replace(u'/all', u'')
        return result
    
    


class TvdbImageHandler(ImageHandler):
    def __init__(self, entity_manager, url):
        ImageHandler.__init__(self, entity_manager, entity_manager.configuration.service['tvdb']['urls']['Banner.getImage'].format(url))
        self.logger = logging.getLogger('Tvdb Image Handler')
    
    



def update_int_property(key, value, entity):
    result = False
    if key and value:
        try:
            value = int(value)
        except ValueError:
            value = None
        if value:
            result = True
            entity[key] = value
    return result


def update_float_property(key, value, entity):
    result = False
    if key and value:
        try:
            value = float(value)
        except ValueError:
            value = None
        if value:
            result = True
            entity[key] = value
    return result


def update_string_property(key, value, entity):
    result = False
    if key and value:
        if not isinstance(value, unicode):
            value = unicode(value, 'utf-8')
        value = value.strip()
        if value:
            result = True
            entity[key] = value
    return result


def update_date_property(key, value, entity):
    result = False
    if key and value:
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            value = None
        if value:
            result = True
            entity[key] = value
    return result


def update_timestamp_property(key, value, entity):
    result = False
    if key and value:
        try:
            value = float(value)
        except ValueError:
            value = None
        if value:
            result = True
            entity[key] = datetime.fromtimestamp(value)
    return result


def format_tmdb_query(value):
    result = None
    if value is not None:
        value = collapse_whitespace.sub(u'+', value)
    return value


def remove_accents(value):
    value = value.strip()
    nkfd_form = unicodedata.normalize('NFKD', value)
    return u''.join([c for c in nkfd_form if not unicodedata.combining(c)])


def make_small_name(name):
    result = None
    if name:
        name = collapse_whitespace.sub(u' ', name).strip()
        result = characters_to_exclude_from_filename.sub(u'', name)
        if not result:
            result = replace_invalid_characters(name)
        result = result.lower()
    return result


def replace_invalid_characters(value):
    if value:
        value = value.replace(u'?', u'question mark')
        value = value.replace(u'*', u'asterisk')
        value = value.replace(u'.', u'period')
        value = value.replace(u':', u'colon')
    return value



string_key_string_pair = re.compile(u'^([^:]+):(.*)$', re.UNICODE)
numberic_key_string_pair = re.compile(u'^([0-9]+):(.+)$', re.UNICODE)
tvdb_list_seperators = re.compile(ur'\||,', re.UNICODE)
strip_space_around_seperator = re.compile(ur'\s*\|\s*', re.UNICODE)
collapse_whitespace = re.compile(ur'\s+', re.UNICODE)
url_to_cache = re.compile(ur'http:/', re.UNICODE)
image_http_type = re.compile(ur'image/.*', re.UNICODE)
characters_to_exclude_from_filename = re.compile(ur'[\\\/?<>:*|\'"^\.]')