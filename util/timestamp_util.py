import datetime
from google.protobuf.timestamp_pb2 import Timestamp


class TimestampUtil:

    @staticmethod
    def get_proto_timestamp(created_datetime: datetime.datetime) -> Timestamp:
        created_datetime = created_datetime.replace(tzinfo=None)
        created: Timestamp = Timestamp()
        created.FromDatetime(created_datetime)
        return created

    @staticmethod
    def get_current_proto_timestamp() -> Timestamp:
        return Timestamp()
