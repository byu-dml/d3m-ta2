from search_process import SearchProcess
from generated_grpc import core_pb2
import uuid
from ta2_server import CoreSession


class TestQueue:
    
    @staticmethod
    def test_queue_ordering():
        core_session = CoreSession(0)
        search_solutions_request = core_pb2.SearchSolutionsRequest(priority=0)
        low_priority_search = SearchProcess(uuid.uuid4(), search_solutions_request)
        search_solutions_request = core_pb2.SearchSolutionsRequest(priority=1)
        high_priority_search = SearchProcess(uuid.uuid4(), search_solutions_request)
        search_solutions_request = core_pb2.SearchSolutionsRequest(priority=100)
        highest_priority_search = SearchProcess(uuid.uuid4(), search_solutions_request)
        
        core_session.insert_into_queue(low_priority_search)
        core_session.insert_into_queue(high_priority_search)
        core_session.insert_into_queue(highest_priority_search)
        
        work_queue = core_session.work_queue

        search = work_queue.get()
        assert search.search_id == highest_priority_search.search_id, 'Search with lower priority at the top of the queue'
        search = work_queue.get()
        assert search.search_id == high_priority_search.search_id, 'Search with lower priority at the top of the queue'
        search = work_queue.get()
        assert search.search_id == low_priority_search.search_id, 'Higher priority search not on queue'
        