# Video Streaming Client-Server application

Implemented using Python + OpenCV + ZeroMQ's Publisher-Subscriber socket pattern.
 
- Any number of clients can connect to the stream, it's supported by ZMQ's pubsub pattern.
- Server and its client(s) can be launched in any order. Client(s) will wait for timeout ms till the server is online and streaming, if the server was down at the time client was launched. Server can run with no clients at all.
- If the client cannot receive anything from the server for more than timeout = 10s by default, the server is considered to be down or disconnected from network and the client(s) are terminated.
- Clients can be launched and stopped, this will have no effect on the stream.
- Video-source is:
  - webcam stream by default;
  - a video-file; in that case the stream will finish naturally at the end of the video.
- Server-side streaming can be terminated by closing the window with stream (by pressing letter q (NB: keyboard layout) or clicking cross(X) on the window). This will automatically disconnect all clients, because there's nothing to watch.

Required libraries are listed in requirements.txt.

Server and client are command line runnable, you can pass the arguments by their keys (see streamer.py --help or watcher.py -- help).

All arguments have their default values for application to launch locally and stream video from webcam, but one can set arguments using keys (--ip --port --source for streamer.py and --ip --port --timeout for watcher.py).

Installation:
```bash
git clone https://github.com/kaustika/zmq_streaming.git
cd zmq_streaming
python -m venv env
source env/bin/activate # Windows: env/Scripts/activate.bat
pip install -r requirements.txt
```

Basic usage:
```bash
cd src
python streaming.py
python watching.py
```

Enjoy your stream!
