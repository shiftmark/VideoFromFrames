"""Server listening for grpc requests."""
import os
from concurrent import futures
import threading
import time
import grpc
import imgstream_pb2_grpc as pb_rpc
import imgstream_pb2 as pb
from pathlib import Path

RPC_SERVER = 'localhost:9999'  # os.environ['RPC_SERVER']
PORT = RPC_SERVER.split(":")[-1]
SERVE_ON = f'0.0.0.0:{PORT}'
FRAMES_DIR_PATH = '/home/adrian/PycharmProjects/grpc/frames'  # os.environ['FRAMES_DIR_PATH']


class Listener(pb_rpc.ImgStreamServicer):
    """
    Listener which implements the rpc call, per .proto file.
    """
    img_dir_path = FRAMES_DIR_PATH

    def __init__(self, img_dir_path: str = img_dir_path):
        img_dir_path = img_dir_path if img_dir_path[-1] == "/" else img_dir_path + "/"
        assert Path(img_dir_path).is_dir(), f"The frames dir path provided is not valid: {img_dir_path}." \
                                            f"Check environment configuration in .env file."
        self.img_dir_path = img_dir_path

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def retrieve_object_bytes(obj_path):

        if '://' in obj_path:
            raise NotImplementedError

        else:
            with open(obj_path, 'rb') as o:
                obj_bytes = o.read()

        return obj_bytes

    def stream(self, request, context):
        """
        Overwrite the stream from pb_rpc.ImgStreamServicer.
        :param request: The request data.
        :param context: not implemented.
        :return: Response with data requested.
        """
        img_id = request.img_id
        # TODO: other image types?
        img_path = f'{self.img_dir_path}frame{img_id}.jpg'
        # read image as bytes without changing compression
        img_data = self.retrieve_object_bytes(obj_path=img_path)
        return pb.Res(img_id=img_id, img_data=img_data)


def serve_grpc(listen_on):
    """
    Opens the socket. Listens for incoming grpc packets.
    """

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    pb_rpc.add_ImgStreamServicer_to_server(Listener(), server)
    server.add_insecure_port(listen_on)
    server.start()
    try:
        while True:
            print(f"Thread-count {threading.active_count()}, listening on {listen_on}")
            time.sleep(10)
    except KeyboardInterrupt:
        server.stop(0)
        print("Exited.")


if __name__ == "__main__":
    serve_grpc(SERVE_ON)
