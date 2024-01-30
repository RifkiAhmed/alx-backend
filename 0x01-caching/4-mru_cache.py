#!/usr/bin/env python3
'''MRUCache Model'''

BaseCaching = __import__('base_caching').BaseCaching


class MRUCache(BaseCaching):
    '''MRUCache CLass'''
    my_cache = {}

    def put(self, key, item):
        '''Add an item in the cache'''
        if key and item:
            keys = list(self.my_cache.keys())
            if len(keys) >= BaseCaching.MAX_ITEMS:
                del self.cache_data[keys[-1]]
                del self.my_cache[keys[-1]]
                print('DISCARD:', keys[-1])
            self.cache_data[key] = item
            self.my_cache[key] = item

    def get(self, key):
        '''Get an item by key'''
        if self.cache_data.get(key):
            item = self.my_cache[key]
            del self.my_cache[key]
            self.my_cache[key] = item
            return self.cache_data[key]
        return None
