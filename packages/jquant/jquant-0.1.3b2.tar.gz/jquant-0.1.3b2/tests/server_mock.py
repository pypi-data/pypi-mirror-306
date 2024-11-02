import asyncio
import time
from concurrent import futures

import grpc
from google.protobuf import any_pb2 as anypb
from google.protobuf import message

from jquant import grpcpb, pb


class StreamService(grpcpb.StreamServiceServicer):
    async def Subscribe(self, request_iterator, context):
        async for req in request_iterator:
            print(f"Received: {req.method}")
            reply = pb.GetTickersReply(timestamp=int(time.time() * 1000), result=[])
            any = anypb.Any()
            any.Pack(reply)
            response = pb.SubscribeReply(
                id=req.id,
                result=any,
            )
            await context.write(response)


async def serve():
    server = grpc.aio.server()
    grpcpb.add_StreamServiceServicer_to_server(StreamService(), server)
    server.add_insecure_port("[::]:50051")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    asyncio.run(serve())
