import typing
from search_solution import SearchSolution
import uuid
from generated_grpc import core_pb2


class SearchProcess(object):
    def __init__(self, search_id: uuid, request: core_pb2.SearchSolutionsRequest, priority: int=0):
        self.search_id = search_id
        self.search_request = request
        self.priority = priority
        self.solutions: typing.Dict[str, SearchSolution] = {}
