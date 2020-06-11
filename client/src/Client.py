import random
import logging
import common.ConfigParser

import grpc

import pb.main_pb2
import pb.main_pb2_grpc



if __name__ == "__main__":
    channel = grpc.insecure_channel('localhost:{}'.format(common.ConfigParser.parse('server', key='Port')))
    stub = pb.main_pb2_grpc.MainStub(channel)
    test = pb.main_pb2.User(name='crisb0')
    print(stub.HelloWorld(test))