#!/usr/bin/env python3
'''LFUCache Model'''

BaseCaching = __import__('base_caching').BaseCaching


class LFUCache(BaseCaching):
    '''LFUCache CLass'''
    my_cache = {}

    def put(self, key, item):
        '''Add an item in the cache'''
        if key and item:
            keys = list(self.my_cache.keys())
            if len(keys) >= BaseCaching.MAX_ITEMS:
                min_value = min(self.my_cache.values())
                for _key, _value in self.my_cache.items():
                    if _value == min_value:
                        v_key = _key
                        break
                del self.cache_data[v_key]
                del self.my_cache[v_key]
                print('DISCARD:', v_key)
            self.cache_data[key] = item
            self.my_cache[key] = 0

    def get(self, key):
        '''Get an item by key'''
        if self.cache_data.get(key):
            item = self.my_cache[key]
            del self.my_cache[key]
            self.my_cache[key] = item + 1
            return self.cache_data[key]
        return None
