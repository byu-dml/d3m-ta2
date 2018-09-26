import threading
import logging
import queue
import time
from search_process import SearchProcess
from search_solution import SearchSolution


class SearchWorker(threading.Thread):
    def __init__(self, search_queue: queue.PriorityQueue, search_processes, name: str):
        super(SearchWorker, self).__init__(name=name)
        self.search_queue = search_queue
        self.search_process: SearchProcess = None
        self.interrupted: bool = False
        self.search_processes = search_processes

    def interrupt(self) -> None:
        logging.info('Worker interrupted')
        self.interrupted = True

    def update_search_solution(self, search_solution: SearchSolution):
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
            return

        logging.info(f'Starting search {self.search_process.search_id}')
        search_solution = SearchSolution()
        self.update_search_solution(search_solution)
        search_solution.start_running()
        time.sleep(3)
        search_solution.complete()
        logging.info(f'Finished search {self.search_process.search_id}')
        self.mark_search_complete()

    def mark_search_complete(self):
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
                self.search_process = self.search_queue.get()
                self.search()
            else:
                # logging.debug("Queue empty sleeping")
                time.sleep(1)
