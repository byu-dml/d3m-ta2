import typing
import uuid
from wrapper.core.progress import Progress


class SearchProcess(object):
    def __init__(self, search_id: uuid, priority: int):
        self.search_id: str = search_id
        self.priority: int = priority
        self.completed: bool = False
        self.progress: Progress = Progress()
        self.should_stop = False
        self.mongo_id = None

    def __lt__(self, other):
        return self.priority > other.priority

    def to_json_structure(self) -> typing.Dict:
        json_structure = {
            'search_id': self.search_id,
            'priority': self.priority,
            'completed': self.completed,
            'progress': self.progress.to_json_structure(),
            'should_stop': self.should_stop
        }
        if self.mongo_id is not None:
            json_structure['_id'] = self.mongo_id
        return json_structure

    @staticmethod
    def from_json_structure(json_structure):
        search_process = SearchProcess(json_structure['search_id'], json_structure['priority'])
        search_process.completed = json_structure['completed']
        search_process.progress = Progress.from_json_structure(json_structure['progress'])
        search_process.should_stop = json_structure['should_stop']
        if '_id' in json_structure:
            search_process.mongo_id = json_structure['_id']

        return search_process
