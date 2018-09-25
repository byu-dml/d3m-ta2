from util.timestamp_util import TimestampUtil

UNKNOWN = 0
PENDING = 1
RUNNING = 2
COMPLETED = 3
ERRORED = 4


class Progress:

    def __init__(self):
        self.state: int = UNKNOWN
        self.status = None
        self.start = None
        self.end = None

    def complete(self):
        self.state = COMPLETED
        self.end = TimestampUtil.get_current_proto_timestamp()

    def start_running(self):
        self.state = PENDING
        self.start = TimestampUtil.get_current_proto_timestamp()
