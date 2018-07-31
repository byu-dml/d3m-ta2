from concurrent import futures
import time

import grpc

import core_pb2
import core_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Core(core_pb2_grpc.CoreServicer):

	def SearchSolutions(self, request, context):
		return core_pb2.SearchSolutionsResponse(search_id='1234567890123456789012345678901234567890')

def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	core_pb2_grpc.add_CoreServicer_to_server(Core(), server)
	server.add_insecure_port('[::]:50052')
	server.start()
	try:
		while True:
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == '__main__':
	serve()