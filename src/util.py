from typing import Any
import os
import cv2


def is_closed_window(win_name: str) -> bool:
    """
    Checks if any signal to close the window was received (letter q in focus
    on the window was pressed or the cross(X) was clicked on).
    :param win_name: name of the window to check;
    :return: True if closed, False if opened.
    """
    is_pressed_q = cv2.waitKey(1) == ord("q")
    is_pressed_x = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) == 0
    return is_pressed_q or is_pressed_x
