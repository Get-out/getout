import random
import itertools

import requests

from atlas_api.helpers import cached_property
from atlas_api.species import Species

class Location(object):
    """Represents a location"""
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

