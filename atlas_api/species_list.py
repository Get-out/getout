from atlas_api.location import Location

class SpeciesList(object):
    """Knows how to get species for a location given a particular distribution of weightings"""
    def __init__(self, location, species_weights, simple_names=False):
        self.location = location
        self.species_weights = species_weights
        self.simple_names = simple_names

    def retreive(self, amount):
        """Retrieve a number of species"""
        species_weight = {x : int(self.species_weights.get(x, 5)) for x in ("bird", "plant", "tree")}

        # Don't include fish unless the user really wants it
        # More likely that user is looking at an area not around water
        # We should probably do geo-magic to work that out
        species_weight['fish'] = int(self.species_weights.get('fish', 0))

        # Land_animal maps to other
        species_weight['other'] = int(self.species_weights.get('land_animal', 5))
        return Location(self.location).ranked_species(10, species_weight, self.simple_names)

