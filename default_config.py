import logging


class Config:
    server_host = 'localhost'
    server_port = '45042'
    log_level = logging.INFO
    num_search_workers = 5
    num_server_request_workers = 10
