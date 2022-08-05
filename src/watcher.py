from util import is_closed_window
from typing import Tuple
import cv2
import zmq


def set_up_client_socket(ip: str, port: str) -> Tuple[zmq.Context, zmq.Socket]:
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
    return context, socket


def watch(context: zmq.Context, socket: zmq.Socket) -> None:
    """
    Watch the video stream being transmitted to socket.
    :param context: connection context;
    :param socket: monitored socket;
    :return:
    """
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
    context, socket = set_up_client_socket(ip="localhost", port="5577")
    watch(context, socket)
