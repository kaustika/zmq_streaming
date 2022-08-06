from util import is_closed_window
from typing import Tuple
import argparse
import cv2
import zmq


def set_up_client_socket(ip: str,
                         port: str) -> Tuple[zmq.Context, zmq.Socket]:
    """
    Sets up client subscriber socket at given ip:port to receive all types
    of messages.
    :param ip: ip-address to connect socket to;
    :param port: port to connect socket to;
    :return: Context and Socket objects to take control over the connection.
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{ip}:{port}")
    # '' - no message filter for subscription
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    print(f"Subscribing to socket at tcp://{ip}:{port}...")
    return context, socket


def check_connection(socket: zmq.Socket) -> None:
    """
    Checks connection by receiving a message from server.
    :param socket: socket to check connection at;
    :return:
    """
    print("Checking connection...")
    _ = socket.recv_pyobj()
    print("Connected!")


def watch(context: zmq.Context,
          socket: zmq.Socket) -> None:
    """
    Watch the video stream being transmitted to socket.
    :param context: connection context;
    :param socket: monitored socket;
    :return:
    """
    check_connection(socket)
    while True:
        frame = socket.recv_pyobj()
        if frame is None:
            print("Server stopped streaming, exiting...")
            break
        cv2.imshow("WATCHING", frame)
        if is_closed_window("WATCHING"):
            break
    socket.close()
    context.term()

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Video Stream Watcher',
                                     add_help=False)
    parser.add_argument("-i", "--ip", action="store", dest="ip",
                        help="Ip-address to connect socket to.",
                        default="localhost")
    parser.add_argument("-p", "--port", action="store", dest="port",
                        help="Port to connect socket to.",
                        default=5577)
    parser.add_argument("-h", "--help", action="help",
                        help="show this help message")
    args = parser.parse_args()

    context, socket = set_up_client_socket(ip=args.ip, port=args.port)
    watch(context, socket)
