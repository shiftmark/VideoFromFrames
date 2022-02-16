# Intro / scope

Serialize image -> transport -> deserialize image => combine all transported images in a video file.

| ![](diagram.png)  |
|:-----------------:|



Notes:

- The files are expected to be compressed. If messages are bigger than 1MB, the transport performance is affected.
- cv2 builds the video from images. The workflow on the client is:   bytes -> PIL -> numpy array -> cv2.
- The server opens the requested image as bytes (ignores compression) and sends it to client (protobuf).
- Naming the output file is not implemented. At the moment the naming pattern is `video<PID-how-created-it>.mp4`

# Setup

### Build the container image (used for both, server and client):

- Execute build.sh file (under Linux run `chmod +x build.sh && ./build.sh`)

### Environment config:

- Set the required environment variables in a `config/.env` file. See the example file: `config/.env.example`
- At the moment frames, are combined from `frames` folder, on the server host. Make sure the images are there.

### Run the server:

- Navigate to `server` folder and run `docker-compose up`

### Run the client:

- Navigate to `client` folder and run `docker-compose up`
- Multiprocessing `multi_client.py` has been implemented for testing purposes. At the moment all processes are doing the same work.

# Usage

The current implementation requires one mandatory update the `.env`:

- `RPC_SERVER` This value should be replaced with the IP or URL of the server.

When starting the client, it will request the frames from the server, using the indexes set to `FIRST_FRAME_ID` and `LAST_FRAME_ID`
If the last frame id is greater than the ids available, you will get an error but the video will be saved, up until the last available frame.
The id is the number before the extension. See the `frames` folder.

# Performance

Without the network bottleneck:

- 367 color images (1920x1080 jpg) to mp4 (30 fps) took about 8.1 seconds. RAM usage is insignificant. Ryzen 9 CPU.
