import queue
from search_process import SearchProcess
from generated_grpc import core_pb2
import uuid


class TestQueue:
    
    @staticmethod
    def test_queue_ordering():
        work_queue = queue.PriorityQueue()
        search_solutions_request = core_pb2.SearchSolutionsRequest(priority=0)
        low_priority_search = SearchProcess(uuid.uuid4(), search_solutions_request)
        search_solutions_request = core_pb2.SearchSolutionsRequest(priority=1)
        high_priority_search = SearchProcess(uuid.uuid4(), search_solutions_request)
        
        work_queue.put(low_priority_search)
        work_queue.put(high_priority_search)
        
        search = work_queue.get()
        assert search.search_id == high_priority_search.search_id, 'Search with lower priority at the top of the queue'
        search = work_queue.get()
        assert search.search_id == low_priority_search.search_id, 'Higher priority search not on queue'
        