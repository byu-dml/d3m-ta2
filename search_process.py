import typing
from search_solution import SearchSolution


class SearchProcess(object):
    def __init__(self, search_id, request, priority=0):
        self.search_id = search_id
        self.search_request = request
        self.priority = priority
        self.solutions: typing.Dict[str, SearchSolution] = {}
