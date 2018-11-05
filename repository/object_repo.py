import redis
import typing
import logging
import json

from search_process import SearchProcess
from search_solution import SearchSolution

REDIS_HOST = 'ta2-redis'
REDIS_PORT = 6379


class ObjectRepo:

    def __init__(self):
        self.client = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            password='')

    def save_search_process(self, search_process: SearchProcess) -> None:
        json_structure = search_process.to_json_structure()
        self.client.execute_command('JSON.SET', search_process.search_id, '.', json.dumps(json_structure))

    def get_search_process(self, search_id) -> typing.Optional[SearchProcess]:
        search_process = None
        json_structure = None
        try:
            json_structure = json.loads(self._get_json(search_id))
            if json_structure is not None:
                search_process = SearchProcess.from_json_structure(json_structure)
        except Exception as e:
            logging.warning(f'Failed to deserialize search process {search_id} {json_structure} {str(e)}')
            pass
        return search_process

    def save_search_solution(self, search_solution: SearchSolution) -> None:
        json_structure = search_solution.to_json_structure()
        self.client.execute_command('JSON.SET', search_solution.id_, '.', json.dumps(json_structure))

    def get_search_solution(self, search_solution_id) -> typing.Optional[SearchSolution]:
        search_solution = None
        json_structure = None
        try:
            json_structure = json.loads(self._get_json(search_solution_id))
            if json_structure is not None:
                search_solution = SearchSolution.from_json_structure(json_structure)
        except Exception as e:
            logging.warning(f'Failed to deserialize search solution {search_solution_id} {json_structure} {str(e)}')
            pass

        return search_solution

    def _get_json(self, key):
        return self.client.execute_command('JSON.GET', key)

    def _set(self, key, object_):
        return self.client.set(key, object_)

    def delete(self, key):
        return self.client.delete(key)
