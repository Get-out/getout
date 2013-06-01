import requests

from atlas_api.helpers import cached_property
from atlas_api import families

class Species(object):
    """Represents a single species"""
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
        return self._from_json['family'].lower() in families.FISH_FAMILIES

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
                return family.split('_')[0].lower()
        return 'other'

    def as_json(self):
        return {'name':self.common_name, 'scientific_name':self.name, 'image':self.image}

