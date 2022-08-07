from contextlib import contextmanager
from util import is_closed_window
from typing import Optional
import argparse
import cv2
import zmq

STREAMER_WIN_NAME = "STREAMING"


@contextmanager
def server_socket_manager(ip: str,
                          port: str) -> zmq.Socket:
    """
    Resource manager for server socket and context.
    :param ip: ip-address to bind socket to;
    :param port: port to bind socket to;
    :return: Socket object to take control over the connection.
    """
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://{ip}:{port}")
    print(f"Accepting connections from {ip} at port {port}"
          f" - tcp://{ip}:{port}")
    try:
        yield socket
    finally:
        socket.close()
        context.term()


def stream(socket: zmq.Socket,
           source: Optional[str]) -> None:
    """
    Stream video (either from webcam or from file) at given socket.
    :param socket: transmitting socket;
    :param source: where to take the video from (0 for webcam or
                   <valid_video_path> for file-content streaming);
    :return:
    """
    source = 0 if not source else source
    video = cv2.VideoCapture(source)

    while True:
        success, frame = video.read()
        if not success:
            print("Check accessibility of your video source! It's "
                  "either the end of the video you passed as source "
                  "or there's something wrong with your webcam.")
            break
        socket.send_pyobj(frame)
        cv2.imshow(STREAMER_WIN_NAME, frame)
        if is_closed_window(STREAMER_WIN_NAME):
            print("Stream window was closed, goodbye! "
                  "All clients are terminated.")
            break

    # stream was ended manually, send None as a signal for that
    socket.send_pyobj(None)

    video.release()
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Video Streamer',
                                     add_help=False)
    parser.add_argument("-i", "--ip", action="store", dest="ip",
                        help="Ip-address to bind socket to.",
                        default="*")
    parser.add_argument("-p", "--port", action="store", dest="port",
                        help="Port to bind socket to.",
                        default=5577)
    parser.add_argument("-s", "--source", action="store", dest="source",
                        help="Where to take the video from:"
                             " - default is None for webcam;"
                             " - <valid_video_path> for file-content streaming.",
                        default=None)
    parser.add_argument("-h", "--help", action="help",
                        help="show this help message")
    args = parser.parse_args()

    try:
        with server_socket_manager(ip=args.ip, port=args.port) as socket:
            stream(socket, args.source)
    except zmq.ZMQError as e:
        print(e)


if __name__ == "__main__":
    main()
