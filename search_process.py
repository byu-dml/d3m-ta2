import typing
from search_solution import SearchSolution
import uuid
from generated_grpc import core_pb2
from wrapper.progress import Progress


class SearchProcess(object):
    def __init__(self, search_id: uuid, request: core_pb2.SearchSolutionsRequest):
        self.search_id: str = search_id
        self.search_request: core_pb2.SearchSolutionsRequest = request
        self.priority: int = request.priority
        self.solutions: typing.Dict[str, SearchSolution] = {}
        self.completed: bool = False
        self.progress: Progress = Progress()
        self.should_stop = False

    def __lt__(self, other):
        return self.priority > other.priority

    def add_search_solution(self, search_solution: SearchSolution):
        self.solutions[search_solution.id_] = search_solution
