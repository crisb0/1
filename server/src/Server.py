from concurrent import futures
import time
import math
import logging
import common.ConfigParser as cfg

import grpc

import pb.main_pb2
import pb.main_pb2_grpc

def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  pb.main_pb2_grpc.add_MainServicer_to_server(
      pb.main_pb2_grpc.MainServicer(), server)
  server.add_insecure_port('[::]:{}'.format(cfg.parse('server', key='Port')))
  server.start()
  server.wait_for_termination()


if __name__ == "__main__":
  serve()