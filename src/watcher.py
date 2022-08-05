import cv2
import zmq
from typing import Tuple
from util import is_closed_window


def set_up_client_socket(ip: str, port: str) -> Tuple[zmq.Context, zmq.Socket]:
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect(f"tcp://{ip}:{port}")
    # '' - no message filter for subscription
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    return context, socket


if __name__ == "__main__":
    context, socket = set_up_client_socket(ip="localhost", port="5577")
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
