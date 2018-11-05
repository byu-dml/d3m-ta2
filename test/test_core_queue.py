from search_process import SearchProcess
from generated_grpc import core_pb2
import uuid


class TestCoreQueue:

    @staticmethod
    def test_queue_ordering(no_worker_core_session):
        low_priority_search = SearchProcess(str(uuid.uuid4()), priority=0)
        high_priority_search = SearchProcess(str(uuid.uuid4()), priority=1)
        highest_priority_search = SearchProcess(str(uuid.uuid4()), priority=100)

        work_queue = no_worker_core_session.work_queue
        assert len(no_worker_core_session.search_processes) == 0, 'There should be no search processes yet'

        no_worker_core_session.add_search_process(low_priority_search)
        no_worker_core_session.add_search_process(high_priority_search)
        no_worker_core_session.add_search_process(highest_priority_search)

        search = work_queue.get()
        assert search.search_id == highest_priority_search.search_id, 'Search with lower priority at the top of the queue'
        search = work_queue.get()
        assert search.search_id == high_priority_search.search_id, 'Search with lower priority at the top of the queue'
        search = work_queue.get()
        assert search.search_id == low_priority_search.search_id, 'Incorrect search returned'
        assert len(no_worker_core_session.search_processes) == 3, 'Search Processes were not added to the dict'
