import cv2
import zmq


context = zmq.Context()
socket = context.socket(zmq.SUB)

print("Connecting to webcam stream...")
socket.connect("tcp://localhost:5577")

# '' - no message filter for subscription
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    frame = socket.recv_pyobj()
    if frame is None:
        break
    cv2.imshow("WATCHING", frame)
    if cv2.waitKey(1) == ord("q") or\
            cv2.getWindowProperty("WATCHING", cv2.WND_PROP_VISIBLE) <= 0:
        break

cv2.destroyAllWindows()
