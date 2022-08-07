from contextlib import contextmanager
from util import is_closed_window
import argparse
import cv2
import zmq

WATCHER_WIN_NAME = "WATCHING"


@contextmanager
def client_socket_manager(ip: str,
                          port: str,
                          timeout: int) -> zmq.Socket:
    """
    Resource manager for client socket and context.
    :param ip: ip-address to connect socket to;
    :param port: port to connect socket to;
    :param timeout: server response timeout in ms;
    :return: Socket object to take control over the connection.
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{ip}:{port}")
    # '' - no message filter for subscription
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    print(f"Subscribing to socket at tcp://{ip}:{port}...")
    try:
        yield socket
    finally:
        socket.close()
        context.term()


def watch(socket: zmq.Socket) -> None:
    """
    Watch the video stream being transmitted to socket.
    :param socket: monitored socket;
    :return:
    """
    while True:
        frame = socket.recv_pyobj()
        if frame is None:
            print("Server stopped streaming, exiting...")
            break
        cv2.imshow(WATCHER_WIN_NAME, frame)
        if is_closed_window(WATCHER_WIN_NAME):
            print("Stream window was closed, goodbye!")
            break
    cv2.destroyAllWindows()


def main():
    parser = argparse.ArgumentParser(description='Video Stream Watcher',
                                     add_help=False)
    parser.add_argument("-i", "--ip", action="store", dest="ip",
                        help="Ip-address to connect socket to.",
                        default="localhost")
    parser.add_argument("-p", "--port", action="store", dest="port",
                        help="Port to connect socket to.",
                        default=5577)
    parser.add_argument("-t", "--timeout", action="store", dest="timeout",
                        help="Server response timeout is ms.",
                        default=5000)
    parser.add_argument("-h", "--help", action="help",
                        help="show this help message")
    args = parser.parse_args()

    try:
        with client_socket_manager(ip=args.ip, port=args.port, timeout=args.timeout) as socket:
            watch(socket)
    except zmq.ZMQError as e:
        print("Timeout for waiting exceeded, server not online, exiting...")
        print(e)


if __name__=="__main__":
    main()
