from concurrent import futures
import time
import math
import logging

import grpc

import pb.main_pb2
import pb.main_pb2_grpc

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pb.main_pb2_grpc.add_MainServicer_to_server(
      MainServicer(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
  serve()