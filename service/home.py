# -*- coding: utf-8 -*-

from datetime import datetime
from service import ResourceHandler

class HomeHandler(ResourceHandler):
    def __init__(self, resolver, node):
        ResourceHandler.__init__(self, resolver, node)
    
    
    def fetch(self, query):
        if 'depend' in query['match']:
            
            # ensure default language
            query['parameter']['language']
            
            if 'index' in query['branch']:
                # Resolve the dependency document
                dependee = self.resolver.resolve(query['match']['depend'].format(**query['parameter']))
                if dependee is not None:
                    for index in query['branch']['index']:
                        if index in dependee[u'head'][u'genealogy']:
                            query['parameter'][index] = dependee[u'head'][u'genealogy'][index]
                            
                    if 'collect' in query['branch']:
                        for pattern in query['branch']['collect']:
                            try:
                                related = self.resolver.resolve(pattern.format(**query['parameter']))
                            except KeyError, e:
                                self.log.debug(u'Could not create reference uri for pattern %s because parameter %s was missing', pattern, e)
                                
                            if related is not None:
                                for index in query['branch']['index']:
                                    if index in related[u'head'][u'genealogy']:
                                        query['parameter'][index] = related[u'head'][u'genealogy'][index]
                                        
                                # we only need one of the documents in collect
                                break
                    query['source'].append(dependee)
    
    
    def parse(self, query):
        if query['source']:
            # Only create a new home document if the dependency is satisfied
            entry = {
                'branch':query['branch'],
                'record':{
                    u'head':{ u'genealogy':query['parameter'].project('ns.service.genealogy'), },
                }
            }
            
            query['result'].append(entry)
    
    
    def store(self, query):
        for entry in query['result']:
            record = None
            collection = query['repository'].database[entry['branch']['collection']]
            
            # Set the modified date
            entry['record'][u'head'][u'modified'] = datetime.utcnow()
            
            # Build all the resolvable URIs from the genealogy
            entry['record'][u'head'][u'alternate'] = []
            for resolvable in entry['branch']['resolvable']:
                try:
                    link = resolvable['format'].format(**entry['record'][u'head'][u'genealogy'])
                    entry['record'][u'head']['alternate'].append(link)
                    if 'canonical' in resolvable and resolvable['canonical']:
                        entry['record'][u'head']['canonical'] = link
                except KeyError, e:
                    self.log.debug(u'Could not create uri for %s because %s was missing from the genealogy', resolvable['name'], e)
                    
            # Try to locate an existing record
            for uri in entry['record'][u'head'][u'alternate']:
                record = collection.find_one({u'head.alternate':uri})
                if record is not None:
                    break
                    
            # This is an update, we already have an existing record
            if record is not None:
                # Compute the union of the two uri lists
                record[u'head'][u'alternate'] = list(set(record[u'head'][u'alternate']).union(entry['record'][u'head'][u'alternate']))
                
                # Compute the union of the two genealogy dictionaries
                # New computed genealogy overrides the existing
                record[u'head'][u'genealogy'] = dict(record[u'head'][u'genealogy'].items() + entry['record'][u'head'][u'genealogy'].items())
                
            # This is an insert, no previous existing record was found
            else:
                record = entry['record']
                record[u'head'][u'created'] = record[u'head'][u'modified']
                
                # Issue a new id
                record[u'head'][u'genealogy'][u'home id'] = self.resolver.issue(query['repository'].host, self.node['key generator'])
                if 'key' in entry['branch']:
                    record[u'head'][u'genealogy'][entry['branch']['key']] = record[u'head'][u'genealogy'][u'home id']
                    
                    # Rebuild all the resolvable URIs from the genealogy again to account for the assigned id
                    record[u'head'][u'alternate'] = []
                    for resolvable in entry['branch']['resolvable']:
                        try:
                            link = resolvable['format'].format(**record[u'head'][u'genealogy'])
                            record[u'head']['alternate'].append(link)
                            if 'canonical' in resolvable and resolvable['canonical']:
                                record[u'head']['canonical'] = link
                        except KeyError, e:
                            self.log.debug(u'Could not create uri for %s because %s was missing from the genealogy', resolvable['name'], e)
                            
            # Save the record to database
            self.log.debug(u'Storing %s', unicode(record[u'head']))
            collection.save(record)
    

