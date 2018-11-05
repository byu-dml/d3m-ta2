import typing
from search_solution import SearchSolution
import uuid
from generated_grpc import core_pb2
from wrapper.core.progress import Progress


class SearchProcess(object):
    def __init__(self, search_id: uuid, priority: int):
        self.search_id: str = search_id
        # self.search_request: core_pb2.SearchSolutionsRequest = request
        self.priority: int = priority
        self.solutions: typing.List[str] = []
        self.completed: bool = False
        self.progress: Progress = Progress()
        self.should_stop = False

    def __lt__(self, other):
        return self.priority > other.priority

    def add_search_solution(self, search_solution: SearchSolution):
        self.solutions.append(search_solution.id_)

    def to_json_structure(self) -> typing.Dict:
        return {
            'search_id': self.search_id,
            'priority': self.priority,
            'solutions': self.solutions,
            'completed': self.completed,
            'progress': self.progress.to_json_structure(),
            'should_stop': self.should_stop
        }

    @staticmethod
    def from_json_structure(json_structure):
        search_process = SearchProcess(json_structure['search_id'], json_structure['priority'])
        search_process.completed = json_structure['completed']
        search_process.progress = Progress.from_json_structure(json_structure['progress'])
        search_process.solutions = json_structure['solutions']
        search_process.should_stop = json_structure['should_stop']

        return search_process

