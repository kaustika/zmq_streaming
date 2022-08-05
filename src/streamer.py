from util import is_closed_window, is_valid_source
from typing import Union, Tuple
import cv2
import zmq


def set_up_server_socket(ip: str, port: str) -> Tuple[zmq.Context, zmq.Socket]:
    """
    Sets up server publisher socket at given ip:port.
    :param ip: ip-address to bind socket to;
    :param port: port to bind socket to;
    :return: Context and Socket objects to take control over the connection.
    """
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://{ip}:{port}")
    return context, socket


def stream(context: zmq.Context, socket: zmq.Socket,
           source: Union[int, str] = 0) -> None:
    """
    Stream video (either from webcam or from file) at given socket.
    :param context: connection context;
    :param socket: transmitting socket;
    :param source: where to take the video from (0 for webcam or
                   <valid_video_path> for file-content streaming);
    :return:
    """
    if is_valid_source(source):
        video = cv2.VideoCapture(source)
        while True:
            _, frame = video.read()
            socket.send_pyobj(frame)
            cv2.imshow("STREAMING", frame)
            if is_closed_window("STREAMING"):
                break
        # stream was ended manually, send None as a signal for that
        socket.send_pyobj(None)
        socket.close()
        context.term()

        video.release()
        cv2.destroyAllWindows()
    else:
        print("Check accessibility of your video source!")


if __name__ == "__main__":
    contest, socket = set_up_server_socket(ip="*", port="5577")
    stream(contest, socket)
