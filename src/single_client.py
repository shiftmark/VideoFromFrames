"""Client for grpc requests."""
import io
import logging
import os
import time
from pathlib import Path

import cv2
import grpc
import numpy as np
from PIL import Image

from utils import imgstream_pb2 as pb
from utils import imgstream_pb2_grpc as pb_rpc
from utils.helpers import str_to_float, str_to_int

FF_ID = str_to_int(os.environ['FIRST_FRAME_ID'])
LF_ID = str_to_int(os.environ['LAST_FRAME_ID'])
F_IDS = list(range(FF_ID, LF_ID))
FPS = str_to_float(os.environ['FPS'])
VIDEO_DIR_PATH = os.environ['VIDEO_DIR_PATH']
RPC_SERVER = os.environ['RPC_SERVER']
RPC_PORT = os.environ['RPC_PORT']
logging.basicConfig(level=logging.INFO)

assert Path(VIDEO_DIR_PATH).is_dir(), f"The video dir path provided is not valid: {VIDEO_DIR_PATH=}. " \
                                      f"Check value in .env file."
_ = str_to_int(RPC_PORT)


def run(image_ids: list):
    """
    Requests image data for each image id provided. Combine images into a mp4 video.
    :param image_ids: A list of image ids.
    :return: None. Saves the video file to disk.
    """

    vide_name = f'video{os.getpid()}.mp4'
    video_dir_path = VIDEO_DIR_PATH if VIDEO_DIR_PATH[-1] == "/" else VIDEO_DIR_PATH + "/"

    with grpc.insecure_channel(RPC_SERVER + ":" + RPC_PORT) as channel:
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
    """
    Close the stream channel on failure.
    :param channel: The channel open.
    :return: None.
    """
    channel.close()


if __name__ == "__main__":
    start = time.time()
    run(F_IDS)
    logging.info(f'Done in {round(time.time()-start, 2)} seconds.')

