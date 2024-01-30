#!/usr/bin/env python3
'''FIFOCache Module'''

BaseCaching = __import__('base_caching').BaseCaching


class FIFOCache(BaseCaching):
    '''FIFOCache CLass'''

    def put(self, key, item):
        '''Add an item in the cache'''
        if key and item:
            keys = list(self.cache_data.keys())
            if len(keys) >= BaseCaching.MAX_ITEMS:
                del self.cache_data[keys[0]]
                print('DISCARD:', keys[0])
            self.cache_data[key] = item

    def get(self, key):
        '''Get an item by key'''
        if self.cache_data.get(key):
            return self.cache_data[key]
        return None
