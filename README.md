# Video Streaming Client-Server application

Implemented using Python + ZeroMQ's Publisher-Subscriber socket pattern.
 
- Any number of clients can connect to the stream, it's supported by ZMQ's pubsub pattern.
- Server and its client(s) can be launched in any order. Client(s) will wait till the server is online and streaming, if the server was down at the time client was launched. Server can run with no clients at all.
- Clients can be launched and stopped, this will have no effect on the stream.
- Video-source is:
  - webcam stream by default;
  - a video-file; in that case the stream will finish naturally at the end of the video.
- Server-side streaming can be terminated by closing the window with stream (by pressinq letter q or clicking cross(X) on the window). This will automatically disconnect all clients, because there's nothing to watch.

Server and client are command line runnable, you can pass the arguments by their keys (see streamer.py --help or watcher.py -- help). By default everything works locally, but IP's can be set manually.
