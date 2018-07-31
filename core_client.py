from __future__ import print_function

import grpc

import core_pb2
import core_pb2_grpc


def run():
	channel = grpc.insecure_channel('localhost:50052')
	stub = core_pb2_grpc.CoreStub(channel)
	response = stub.SearchSolutions(core_pb2.SearchSolutionsRequest())
	print('Client received: ' + response.search_id)

if __name__ == '__main__':
	run()