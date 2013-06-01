import random
import itertools

import requests

from helpers import cached_property
import families

class Location(object):
    search_url = 'http://spatial.ala.org.au/ws/search/'
    info_url = 'http://spatial.ala.org.au/ws/object/'
    species_url = 'http://biocache.ala.org.au/ws/webportal/species/'

    def __init__(self, name):
        self.name = name

    @cached_property
    def pid(self):
        info = requests.get(self.search_url, params=dict(
            q = self.name,
        )).json()
        return info[0]['pid']

    @cached_property
    def info(self):
        return requests.get(self.info_url + self.pid).json()

    @property
    def bounding_box(self):
        return self.info['bbox']

    @cached_property
    def species(self):
        results = requests.get(self.species_url, params=dict(
            wkt = self.bounding_box,
            pageSize = 1000000,
        )).json()
        return [Species(i) for i in results if i['rank'] == 'species']

    def ranked_species(self, number=10, types={}):
        # sort the species by their sighting counts
        sorted_species = sorted(self.species, key=lambda x: x.count, reverse=True)

        # the percent chance that a certain thing will be shown
        sum_scores = sum(types.values())
        type_scores = {
            k: float(score) / sum_scores
            for k, score in types.iteritems()
        }

        type_ranked = (
            i
            for i in sorted_species
            if random.random() < type_scores[i.le_type]
        )

        return list(itertools.islice(type_ranked, number))

class Species(object):
    info_url = 'http://bie.ala.org.au/species/'

    def __init__(self, json_response):
        self._from_json = json_response

    def __repr__(self):
        return '<Species name:"%s" (%s)>' % (self.common_name, self.name)

    @property
    def count(self):
        return self._from_json['count']

    @property
    def is_fish(self):
        return self._from_json['family'].lower() in FISH_FAMILIES

    @property
    def common_name(self):
        return self._from_json['commonName'] or self.name

    @property
    def name(self):
        return self._from_json['name']

    @property
    def _guid(self):
        return self._from_json['guid']

    @cached_property
    def _info(self):
        return requests.get(self.info_url + self._guid + '.json').json()

    @property
    def image(self):
        images = [i['largeImageUrl'] for i in self._info['images']]
        return images[0] if images else "/static/img/not-found.gif"

    @property
    def description(self):
        # super-reliable way of getting the description
        properties = [i['value'] for i in self._info['simpleProperties'] if not i['value'].startswith("http")]
        return max(properties, key=len) if properties else ""

    @property
    def le_type(self):
        # please forgive me, for I have sinneth
        for family in dir(families):
            if not family.endswith('FAMILIES'):
                continue
            if self._from_json['family'].lower() in getattr(families, family):
                print family.split('_')[0].lower()
                return family.split('_')[0].lower()
        print 'other'
        return 'other'

    def as_json(self):
        return {'name':self.common_name, 'scientific_name':self.name, 'image':self.image}
