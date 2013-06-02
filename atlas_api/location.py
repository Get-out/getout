import itertools
import requests
import random

from atlas_api.helpers import cached_property
from atlas_api.species import Species

class Location404(Exception):
    """Exception to encapsulate a location that doesn't exist"""
    def __init__(self, location):
        self.location = location
        super(Location404, self).__init__()

class Location(object):
    """Represents a location"""
    search_url = 'http://spatial.ala.org.au/ws/search/'
    info_url = 'http://spatial.ala.org.au/ws/object/'
    species_url = 'http://biocache.ala.org.au/ws/webportal/species/'

    def __init__(self, name):
        self.name = name

    @cached_property
    def pid(self):
        """Ask atlas for the pid of this location"""
        info = requests.get(self.search_url
            , params=dict(q = self.name)
            ).json()
        if not info:
            raise Location404(location=self.name)
        return info[0]['pid']

    @cached_property
    def info(self):
        """Ask atlas for info about this location"""
        return requests.get(self.info_url + self.pid).json()

    @cached_property
    def species(self):
        """Ask atlas for all the species in our bounding box"""
        results = requests.get(self.species_url
            , params=dict(wkt = self.bounding_box, pageSize = 1000000)
            )
        return [Species(i) for i in results.json() if i['rank'] == 'species']

    @property
    def bounding_box(self):
        return self.info['bbox']

    def ranked_species(self, number=10, types=None):
        """Return <number> species with a range of types as indicated by <types>"""
        if types is None:
            types = {}

        # sort the species by their sighting counts
        raw_list = self.species
        sorted_species = sorted(raw_list, key=lambda x: x.count, reverse=True)

        # the percent chance that a certain thing will be shown
        sum_scores = sum(types.values())
        type_scores = {
            k: float(score) / sum_scores
            for k, score in types.iteritems()
            }

        # Make a generator to spit out species
        type_ranked = (
            i
            for i in sorted_species
            if random.random() < type_scores[i.le_type]
            )

        # Return only <number> of our list of species
        return list(itertools.islice(type_ranked, number))

