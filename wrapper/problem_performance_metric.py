import generated_grpc.problem_pb2 as grpc_problem


class ProblemPerformanceMetric:
    
    def __init__(self, protobuf_problem_performance_metric: grpc_problem.ProblemPerformanceMetric):
        self.protobuf_problem_performance_metric = protobuf_problem_performance_metric
        self.performance_metric = None
        self.k = None
        self.pos_label = None
    
    
    @staticmethod
    def get_from_protobuf(protobuf_problem_performance_metric: grpc_problem.ProblemPerformanceMetric):
        problem_performance_metric = ProblemPerformanceMetric(protobuf_problem_performance_metric)
        metric = grpc_problem.PerformanceMetric.Name(protobuf_problem_performance_metric.metric)
        problem_performance_metric.performance_metric = metric
        problem_performance_metric.k = protobuf_problem_performance_metric.k
        problem_performance_metric.pos_label = protobuf_problem_performance_metric.pos_label
        
        return problem_performance_metric
        
