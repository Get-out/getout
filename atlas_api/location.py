import requests

from helpers import cached_property

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

    @cached_property
    def bounding_box(self):
        return self.info['bbox']

    @cached_property
    def species(self):
        return requests.get(self.species_url, params=dict(
            wkt = self.bounding_box,
            pageSize = 1000,
        )).json()
