from __future__ import print_function

import logging

import grpc
import chat_pb2
import chat_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:50051')

    # Exercise login
    stub = chat_pb2_grpc.ChatStub(channel)
    login_response = stub.Login(chat_pb2.LoginRequest(name='you'))
    print("Chat client received: " + login_response.token)


    # Exercise logout
    stub.Logout(chat_pb2.LogoutRequest(token=login_response.token))

if __name__ == '__main__':
    logging.basicConfig()
    run()
