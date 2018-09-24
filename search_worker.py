import threading
import logging
import queue
import time
from search_process import SearchProcess

class SearchWorker(threading.Thread):
    def __init__(self, search_queue: queue.PriorityQueue, name):
        super(SearchWorker,self).__init__(name=name)
        self.queue = search_queue
        self.search_process: SearchProcess= None
        self.interrupted: bool = False
    
    def interrupt(self) -> None:
        logging.debug('Worker interrupted')
        self.interrupted = True
    
    def search(self):
        if self.search_process is not None:
            logging.debug(f'Searching search process {self.search_process}')
            time.sleep(3)
            logging.debug("Done searching!")
            self.search_process = None
        else:
            logging.warning("Tried to search with no search process")

    def run(self):
        logging.debug(f'Worker thread {self.name} started')
        while not self.interrupted:
            logging.debug("Checking if queue not empty")
            if not self.queue.empty():
                logging.debug("Grabbing some work")
                priority, self.search_process = self.queue.get()
                self.search()
            else:
                logging.debug("Queue empty sleeping")
                time.sleep(1)
        

