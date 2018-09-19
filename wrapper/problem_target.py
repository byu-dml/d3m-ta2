import generated_grpc.problem_pb2 as grpc_problem


class ProblemTarget:
    
    def __init__(self, protobuf_problem_target: grpc_problem.ProblemTarget):
        self.protobuf_problem_target = protobuf_problem_target
        self.target_index = None
        self.resource_id = None
        self.column_index = None
        self.column_name = None
        self.clusters_number = None
    
    
    @staticmethod
    def get_from_protobuf(protobuf_problem_target: grpc_problem.ProblemTarget):
        problem_target = ProblemTarget(protobuf_problem_target)
        problem_target.target_index = protobuf_problem_target.target_index
        problem_target.resource_id = protobuf_problem_target.resource_id
        problem_target.column_index = protobuf_problem_target.column_index
        problem_target.column_name = protobuf_problem_target.column_name
        problem_target.clusters_number = protobuf_problem_target.clusters_number
        
        return problem_target
        
