"""Client for grpc requests."""
import cv2
import grpc
import io
import logging
import imgstream_pb2_grpc as pb_rpc
import imgstream_pb2 as pb
import os
import numpy as np
import time

from PIL import Image
from pathlib import Path

FF_ID = int('0')  # os.environ['FIRST_FRAME_ID'])
LF_ID = int('367')  # os.environ['LAST_FRAME_ID'])
F_IDS = list(range(FF_ID, LF_ID))
FPS = float('30')  # os.environ['FPS'])
VIDEO_DIR_PATH = '/home/adrian/Desktop'  # os.environ['VIDEO_DIR_PATH']
RPC_SERVER = 'localhost:9999'  # os.environ['RPC_SERVER']


def run(image_ids: list):
    """
    Requests image data for each image id provided. Combine images into a mp4 video.
    :param image_ids: A list of image ids.
    :return: None. Saves the video file to disk.
    """

    vide_name = f'video{os.getpid()}.mp4'
    video_dir_path = VIDEO_DIR_PATH if VIDEO_DIR_PATH[-1] == "/" else VIDEO_DIR_PATH + "/"
    assert Path(video_dir_path).is_dir(), f"The video dir path provided is not valid: {video_dir_path}." \
                                          f"Check environment configuration in .env file."

    with grpc.insecure_channel(RPC_SERVER) as channel:
        stub = pb_rpc.ImgStreamStub(channel)

        first_response = stub.stream(pb.Req(img_id=image_ids[0]))
        first_image = Image.open(io.BytesIO(first_response.img_data))
        size = first_image.size
        video = cv2.VideoWriter(video_dir_path + vide_name, cv2.VideoWriter_fourcc(*'mp4v'), FPS, size)

        for i in image_ids[1:]:
            try:
                response = stub.stream(pb.Req(img_id=i))
                image = Image.open(io.BytesIO(response.img_data))
                assert image.size == size,\
                    f"Image size not the same as first image. {image.size} vs {size}"
                video.write(cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR))

            except Exception as e:
                logging.exception("Exception", e)
                channel.unsubscribe(close)
                exit()

        video.release()


def close(channel):
    channel.close()


if __name__ == "__main__":
    start = time.time()
    run(F_IDS)
    print(time.time()-start)
