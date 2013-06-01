from django.core.cache import cache

def cached_property(f):
    """returns a cached property that is calculated by function f"""
    def get(self):
        uuid = hash("{}{}{}".format(self.__class__.__name__, self.name, f.func_name))

        if uuid not in cache:
            cache.add(uuid, f(self))

        return cache.get(uuid)

    return property(get)

