import cv2
import zmq
import os.path
from typing import Union, Any


def set_up_connection(ip: str, port: str) -> zmq.Socket:
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind(f"tcp://{ip}:{port}")
    return socket


def is_closed_window(win_name: str) -> bool:
    is_pressed_q = cv2.waitKey(1) == ord("q")
    is_pressed_x = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0
    return is_pressed_q or is_pressed_x


def is_valid_source(source: Any) -> bool:
    if not os.path.isfile(source) or source == 0:
        return False
    video = cv2.VideoCapture(source)
    success, _ = video.read()
    return bool(success)


def stream(source: Union[int, str] = 0) -> None:
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
        video.release()
        cv2.destroyAllWindows()
    else:
        print("Check accessibility of your video source!")


if __name__=="__main__":
    socket = set_up_connection(ip="*", port="5577")
    stream()


