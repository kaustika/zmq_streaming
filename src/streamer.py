import cv2
import zmq


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5577")

video = cv2.VideoCapture(0)

while True:
    img, frame = video.read()
    socket.send_pyobj(frame)
    cv2.imshow("STREAMING", frame)
    if cv2.waitKey(1) == ord("q") or\
            cv2.getWindowProperty("STREAMING", cv2.WND_PROP_VISIBLE) <= 0:
        break

socket.send_pyobj(None)
video.release()
cv2.destroyAllWindows()
