#!/usr/bin/env python3
"""Define the start index and the end index for pagination
"""
import csv
import math
from typing import List, Tuple


def index_range(page: int, page_size: int) -> Tuple[int, int]:
    '''Retrun the start index and the the end index'''
    return (page_size * (page - 1), page * page_size)


class Server:
    """Server class to paginate a database of popular baby names.
    """
    DATA_FILE = "Popular_Baby_Names.csv"

    def __init__(self):
        self.__dataset = None

    def dataset(self) -> List[List]:
        """Cached dataset
        """
        if self.__dataset is None:
            with open(self.DATA_FILE) as f:
                reader = csv.reader(f)
                dataset = [row for row in reader]
            self.__dataset = dataset[1:]

        return self.__dataset

    def get_page(self, page: int = 1, page_size: int = 10) -> List[List]:
        '''Return the appropriate page of the dataset'''
        assert isinstance(page, int) and isinstance(page_size, int)
        assert page >= 0 and page_size >= 0
        assert page != 0 and page_size != 0
        indexes: Tuple = index_range(page, page_size)
        return self.dataset()[indexes[0]: indexes[1]]
