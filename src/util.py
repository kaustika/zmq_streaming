import cv2


def is_closed_window(win_name: str) -> bool:
    is_pressed_q = cv2.waitKey(1) == ord("q")
    is_pressed_x = cv2.getWindowProperty(win_name, cv2.WND_PROP_VISIBLE) <= 0
    return is_pressed_q or is_pressed_x
