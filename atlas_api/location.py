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

    @property
    def bounding_box(self):
        return self.info['bbox']

    @cached_property
    def species(self):
        results = requests.get(self.species_url, params=dict(
            wkt = self.bounding_box,
            pageSize = 1000,
        )).json()
        return [Species(i) for i in results if i['rank'] == 'species']

class Species(object):
    info_url = 'http://bie.ala.org.au/species/info/'

    def __init__(self, json_response):
        self._from_json = json_response

    def __repr__(self):
        return '<Species name:"%s" (%s)>' % (self.common_name, self.name)

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
        return requests.get(self.info_url + self._guid + '.json').json()['taxonConcept']

    @property
    def image(self):
        return self._info['image']
