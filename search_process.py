import typing
from search_solution import SearchSolution
import uuid
from generated_grpc import core_pb2


class SearchProcess(object):
    def __init__(self, search_id: uuid, request: core_pb2.SearchSolutionsRequest):
        self.search_id = search_id
        self.search_request = request
        self.priority = request.priority
        self.solutions: typing.Dict[str, SearchSolution] = {}

    def __lt__(self, other):
        return self.priority > other.priority
