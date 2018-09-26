import threading
import logging
import queue
import time
import typing
from search_process import SearchProcess
from search_solution import SearchSolution


class SearchWorker(threading.Thread):
    def __init__(self, search_queue: queue.PriorityQueue,
                 search_processes: typing.Dict[str, SearchProcess],
                 name: str):
        super(SearchWorker, self).__init__(name=name)
        self.search_queue = search_queue
        self.search_process: SearchProcess = None
        self.interrupted: bool = False
        self.search_processes: typing.Dict[str, SearchProcess] = search_processes

    def interrupt(self) -> None:
        logging.info('Worker interrupted')
        self.interrupted = True

    def stop_search(self, search_id: str) -> None:
        if self.search_process is not None and self.search_process.search_id == search_id:
            self.interrupt()

    def _update_search_solution(self, search_solution: SearchSolution) -> None:
        if self.search_process is None:
            logging.warning('No search process to add a solution to')
            return
        self.search_process.solutions[search_solution.id_] = search_solution

    def search(self):
        if self.search_process is None:
            logging.warning("Tried to search with no search process")
            return

        if self.interrupted:
            logging.info(f'Search {self.search_process.search_id} interrupted')
            self.search_process = None
            return

        logging.info(f'Starting search {self.search_process.search_id}')
        search_solution = SearchSolution()
        self._update_search_solution(search_solution)
        search_solution.start_running()
        if self.interrupted:
            logging.info(f'Search {self.search_process.search_id} interrupted')
            self.search_process = None
            return
        time.sleep(3)
        if self.interrupted:
            logging.info(f'Search {self.search_process.search_id} interrupted')
            self.search_process = None
            return
        search_solution.complete()
        logging.info(f'Finished search {self.search_process.search_id}')
        self._mark_search_complete()

    def _mark_search_complete(self):
        if self.search_process is None:
            logging.warning('No search process to mark complete')
            return

        self.search_process.completed = True
        self.search_process = None

    def run(self):
        logging.debug(f'Started {self.name}')
        while not self.interrupted:
            if not self.search_queue.empty():
                logging.debug("Grabbing some work")
                self.search_process: SearchProcess = self.search_queue.get()
                if self.search_process.stopped:
                    logging.debug('Grabbed stopped search process')
                    self.search_process = None
                else:
                    self.search()
            else:
                # logging.debug("Queue empty sleeping")
                time.sleep(1)
