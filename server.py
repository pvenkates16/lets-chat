# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC chat server."""

from concurrent import futures
import logging

import grpc
import chat_pb2
import chat_pb2_grpc
import uuid


class Chat(chat_pb2_grpc.ChatServicer):

    def __init__(self):
        self.user_tokens = dict()
        print("SERVER: Started chat server")

    def Login(self, request, context):
        uid = str(uuid.uuid1())
        self.user_tokens[uid] = request.name
        print("SERVER: Added user %s, token %s" % (self.user_tokens[uid], uid))
        print("SERVER: " + str(self.user_tokens))
        return chat_pb2.LoginResponse(token='%s' % uid)

    def Logout(self, request, context):
        uid = request.token
        print("SERVER: Logging out" + uid)
        name = self.user_tokens[uid]
        del self.user_tokens[uid]    # remove token from our map
        print("SERVER: Byebye, %s, %s!" , uid, name)
        return chat_pb2.LogoutResponse()



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServicer_to_server(Chat(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
