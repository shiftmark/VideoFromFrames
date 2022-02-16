"""Run the client an N processes"""
import os
from multiprocessing import Process

import single_client
from utils.helpers import str_to_int

FF_ID = str_to_int(os.environ['FIRST_FRAME_ID'])
LF_ID = str_to_int(os.environ['LAST_FRAME_ID'])
F_IDS = list(range(FF_ID, LF_ID))
PROCESSES_COUNT = str_to_int(os.environ['PROCESSES_COUNT'])
assert PROCESSES_COUNT > 0, f"The processes count must be > 0. Received {PROCESSES_COUNT=}. " \
                            f"Check value provided in .env file."

if __name__ == "__main__":
    processes_count = PROCESSES_COUNT
    processes = {}
    for proc in range(processes_count):
        processes[proc] = Process(target=single_client.run, args=(F_IDS, ))

    for proc in range(processes_count):
        processes[proc].start()
