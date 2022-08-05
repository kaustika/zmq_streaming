from typing import Any
import os
import cv2


def is_closed_window(win_name: str) -> bool:
    """
    Checks if any signal to close the window was received (letter q in focus
    on the window was pressed or the cross(X) was clicked on).
    :param win_name: name of the window to ckeck;
    :return:
    """
    is_pressed_q = cv2.waitKey(1) == ord("q")
    is_pressed_x = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0
    return is_pressed_q or is_pressed_x


def is_valid_source(source: Any) -> bool:
    """
    Checks if the given source is valid input for cv2.VideoStream. It should
    be either 0 or <valid_video_path> and not cause problems while reading
    the stream.
    :param source: video source to be checked;
    :return:
    """
    if source != 0 and not os.path.isfile(source):
        return False
    video = cv2.VideoCapture(source)
    success, _ = video.read()
    return bool(success)
