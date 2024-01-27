#!/usr/bin/env python3
"""
Define the start index and the end index for pagination
"""


def index_range(page, page_size):
    '''Retrun the start index and the the end index'''
    return (page_size * (page - 1), page * page_size)


# TEST CODE:
# res = index_range(1, 7)
# print(type(res))
# print(res)

# res = index_range(page=3, page_size=15)
# print(type(res))
# print(res)
