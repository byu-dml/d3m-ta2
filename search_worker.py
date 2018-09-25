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

    def search(self):
        if self.search_process is not None:
            logging.info(f'Starting search {self.search_process.search_id}')
            search_solution = SearchSolution()
            search_solution.start_running()
            time.sleep(3)
            search_solution.complete()
            logging.info(f'Finished search {self.search_process.search_id}')
            self.mark_search_complete()
        else:
            logging.warning("Tried to search with no search process")

    def mark_search_complete(self):
        if self.search_process is not None:
            self.search_process.completed = True
            search_id = self.search_process.search_id
            if search_id in self.search_processes:
                self.search_processes[search_id] = self.search_process
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
