from __future__ import print_function

import grpc
import unittest
import json

import core_pb2
import core_pb2_grpc


class GrpcServerTestCase(unittest.TestCase):

	def setUp(self):
		self.protocol_version = core_pb2.DESCRIPTOR.GetOptions().Extensions[core_pb2.protocol_version]
		channel = grpc.insecure_channel('localhost:50052')
		self.stub = core_pb2_grpc.CoreStub(channel)

	def parse_grpc_exception(self, exception):
		exception_properties = json.loads(exception.debug_error_string())
		grpc_message = exception_properties['grpc_message']
		prefix = 'Exception calling application: '
		message = grpc_message[len(prefix):]
		return message

	def test_search_solutions_response(self):
		response_1 = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
		response_2 = self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version=self.protocol_version))
		search_id_1 = response_1.search_id
		search_id_2 = response_2.search_id
		if len(search_id_1) < 22:
			raise ValueError('search_id returned in SearchSolutionsResponse is less than 22 characters')
		self.assertNotEqual(search_id_1, search_id_2, f'Two consecutive calls to SearchSolutions produced the same search_id: {search_id_1}')

		with self.assertRaises(Exception) as cm:
			self.stub.SearchSolutions(core_pb2.SearchSolutionsRequest(version='WRONG_VERSION')).result()
		returned_message = self.parse_grpc_exception(cm.exception)
		expected_error_message = 'TA3 protocol version does not match TA2 protocol version'
		self.assertEqual(returned_message, expected_error_message, 'Did not recieve expected error message for mismatched protocol versions between TA2 and TA3')

	def test_get_search_solutions_results_response(self):
		with self.assertRaises(Exception) as cm:
			self.stub.GetSearchSolutionsResults(core_pb2.GetSearchSolutionsResultsRequest(search_id='WRONG_SEARCH_ID')).result()
		returned_message = self.parse_grpc_exception(cm.exception)
		expected_error_message = 'search_id provided in GetSearchSolutionsResultsRequest does not match any search_process'
		self.assertEqual(returned_message, expected_error_message, 'Did not recieve expected error message for calling GetSearchSolutionsResults with invalid search_id')
		




if __name__ == '__main__':
	test_cases = [GrpcServerTestCase]
	test_suite = unittest.TestSuite(map(unittest.TestLoader().loadTestsFromTestCase, test_cases))
	unittest.TextTestRunner().run(test_suite)