import cv2
import zmq


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5577")

while True:
    video = cv2.VideoCapture(0)

    while True:
        img, frame = video.read()
        socket.send_pyobj(frame)
        cv2.imshow("STREAMING", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
