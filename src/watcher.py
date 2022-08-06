from util import is_closed_window
from typing import Tuple
import numpy as np
import argparse
import cv2
import zmq


def set_up_client_socket(ip: str,
                         port: str,
                         timeout: int) -> Tuple[zmq.Context, zmq.Socket]:
    """
    Sets up client subscriber socket at given ip:port to receive all types
    of messages.
    :param ip: ip-address to connect socket to;
    :param port: port to connect socket to;
    :param timeout: server response timeout in ms;
    :return: Context and Socket objects to take control over the connection.
    """
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{ip}:{port}")
    # '' - no message filter for subscription
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    socket.setsockopt(zmq.RCVTIMEO, timeout)
    print(f"Subscribing to socket at tcp://{ip}:{port}...")
    return context, socket


def receive_object(socket: zmq.Socket) -> np.ndarray:
    """
    Try-catch wrapper for receiving msgs from server.
    Exception is thrown when timeout is exceeded -> server either
    didn't connect at all in the beginning ar lost its network
    connection.
    :param socket: subscriber socket;
    :return:
    """
    try:
        frame = socket.recv_pyobj()
        return frame
    except zmq.ZMQError as e:
        print("Timeout for waiting exceeded, server not online, exiting...")
        print(e)
        exit()


def watch(context: zmq.Context,
          socket: zmq.Socket) -> None:
    """
    Watch the video stream being transmitted to socket.
    :param context: connection context;
    :param socket: monitored socket;
    :return:
    """
    while True:
        frame = receive_object(socket)
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
    parser.add_argument("-t", "--timeout", action="store", dest="timeout",
                        help="Server response timeout is ms.",
                        default=10000)
    parser.add_argument("-h", "--help", action="help",
                        help="show this help message")
    args = parser.parse_args()

    context, socket = set_up_client_socket(ip=args.ip, port=args.port, timeout=args.timeout)
    watch(context, socket)
