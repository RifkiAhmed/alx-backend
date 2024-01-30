#!/usr/bin/env python3
'''BasicCache Model'''


BaseCaching = __import__('base_caching').BaseCaching


class BasicCache(BaseCaching):
    '''BasicCache CLass'''

    def put(self, key, item):
        '''Add an item in the cache'''
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        '''Get an item by key'''
        if self.cache_data.get(key):
            return self.cache_data[key]
        return None
