import typing
import logging
import pymongo
from pymongo.collection import InsertOneResult, DeleteResult, Cursor

from search_process import SearchProcess
from search_solution import SearchSolution


class ObjectRepo:

    def __init__(self):
        self.client = None
        self._search_processes = None
        self._search_solutions = None

    def save_search_process(self, search_process: SearchProcess) -> typing.Union[SearchProcess, InsertOneResult]:
        json_structure = search_process.to_json_structure()
        if search_process.mongo_id is not None:
            query = {'_id': search_process.mongo_id}
            result = self.search_processes.replace_one(query, json_structure, upsert=True)
        else:
            result = self.search_processes.insert_one(json_structure)

        return result

    def get_search_process(self, search_id) -> typing.Optional[SearchProcess]:
        search_process = None
        result = self.search_processes.find_one({'search_id': search_id})
        if result is not None:
            search_process = SearchProcess.from_json_structure(result)

        return search_process

    def save_search_solution(self, search_solution: SearchSolution) -> typing.Union[SearchSolution, InsertOneResult]:
        json_structure = search_solution.to_json_structure()
        if search_solution.mongo_id is not None:
            query = {'_id': search_solution.mongo_id}
            result = self.search_solutions.replace_one(query, json_structure, upsert=True)
        else:
            result = self.search_solutions.insert_one(json_structure)

        return result

    def get_search_solution(self, search_solution_id) -> typing.Optional[SearchSolution]:
        result = self.search_solutions.find_one({'id': search_solution_id})
        search_solution = None
        if result is not None:
            search_solution = SearchSolution.from_json_structure(result)

        return search_solution

    def delete_search_process_and_solutions(self, search_id) -> DeleteResult:
        query = {'search_id': search_id}
        delete_solutions_result = self.search_solutions.delete_many(query)
        logging.debug(f'Deleted {delete_solutions_result.deleted_count} search solutions')
        delete_process_result: DeleteResult = self.search_processes.delete_one(query)
        logging.debug(f'Deleted {delete_process_result.deleted_count} search processes')

        return delete_process_result

    def get_all_solutions_for_search(self, search_id) -> typing.List[SearchSolution]:
        query = {'search_id': search_id}
        documents: Cursor = self.search_solutions.find(query)
        search_solutions = []
        if documents is not None:
            search_solutions = [SearchSolution.from_json_structure(doc) for doc in documents]

        return search_solutions

    def _initialize_client(self):
        if self.client is None:
            self.client = pymongo.MongoClient('ta2-mongodb', 27017)
            self._search_processes = self.client['search_processes']['search_processes']
            self._search_solutions = self.client['search_solutions']['search_solutions']

    @property
    def search_processes(self):
        self._initialize_client()
        return self._search_processes

    @search_processes.setter
    def search_processes(self, value):
        self._search_processes = value

    @property
    def search_solutions(self):
        self._initialize_client()
        return self._search_solutions

    @search_solutions.setter
    def search_solutions(self, value):
        self._search_solutions = value
