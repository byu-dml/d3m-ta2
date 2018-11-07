import multiprocessing
import logging
import time

from repository.object_repo import ObjectRepo
from search_process import SearchProcess
from search_solution import SearchSolution


class SearchWorker(multiprocessing.Process):
    def __init__(self,
                 search_queue: multiprocessing.Queue,
                 name: str):
        super(SearchWorker, self).__init__(name=name)
        self.search_queue = search_queue
        self.search_process: SearchProcess = None
        self.interrupted: bool = False
        self.db = ObjectRepo()

    def interrupt(self) -> None:
        logging.info('Worker interrupted')
        self.interrupted = True

    def should_stop_searching(self) -> bool:
        self._get_latest_search_process()
        if self.search_process is None:
            return True
        return self.search_process is not None and (self.search_process.should_stop or self.interrupted)

    def _update_search_solution(self, search_solution: SearchSolution) -> None:
        if self.search_process is None:
            logging.warning('No search process to add a solution to')
            return
        self.db.save_search_solution(search_solution)

    def search(self) -> None:
        if self.search_process is None:
            logging.warning("Tried to search with no search process")
            return

        self._start_search()
        logging.info(f'Starting search {self.search_process.search_id}')
        for i in range(3):
            if self.should_stop_searching():
                self._remove_search_process()
                return
            search_solution = SearchSolution(self.search_process.search_id)
            logging.debug(f'Adding solution {search_solution.id_}')
            search_solution.start_running()
            self._update_search_solution(search_solution)
            time.sleep(1)
            search_solution.complete(pipeline=None)
            self._update_search_solution(search_solution)

        logging.info(f'Finished search {self.search_process.search_id}')
        self._mark_search_complete()

    def _start_search(self):
        self._get_latest_search_process()
        self.search_process.start()

        self._update_search_process()
        self._get_latest_search_process()

    def stop_search(self, search_id: str) -> None:
        if self.search_process is not None and self.search_process.search_id == search_id:
            self._remove_search_process()

    def _update_search_process(self):
        if self.search_process is not None:
            self.db.save_search_process(self.search_process)

    def _remove_search_process(self) -> None:
        logging.info(f'Search {self.search_process.search_id} interrupted')
        self.search_process.should_stop = True
        self._update_search_process()
        self.search_process = None

    def _mark_search_complete(self) -> None:
        if self.search_process is None:
            logging.warning('No search process to mark complete')
            return

        self._get_latest_search_process()
        self.search_process.complete()
        self._update_search_process()
        self.search_process = None

    def _get_latest_search_process(self):
        if self.search_process is not None:
            self.search_process = self.db.get_search_process(self.search_process.search_id)

    def run(self):
        logging.debug(f'Started {self.name}')
        while not self.interrupted:
            if not self.search_queue.empty():
                self.search_process: SearchProcess = self.search_queue.get()
                logging.debug(f'Grabbed search {self.search_process.search_id}')
                if self.should_stop_searching():
                    if self.search_process is not None:
                        logging.debug(f'Grabbed stopped search process {self.search_process.search_id}')
                    self.search_process = None
                else:
                    self.search()
            else:
                # logging.debug("Queue empty sleeping")
                time.sleep(1)
