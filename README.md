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

Server and client are command line runnable, you can pass the arguments by their keys (see streamer.py --help or watcher.py -- help). By default everything works locally, but IPs can be set manually.

Required libraries are listed in requirements.txt.
- run server: python.exe streamer.py (--ip --port --source)
- run client: python.exe watcher.py (--ip --port --timeout)

Enjoy your stream!
