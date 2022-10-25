import cv2
import numpy as np
import time
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urljoin
from requests.auth import HTTPBasicAuth

load_dotenv()

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent / 100)
    height = int(frame.shape[0] * percent / 100)
    dim = (width, height)
    
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

# Uncoment below if you use IP Camera and comment the next line uncommented
# USER = os.getenv("USER")
# PASSWORD = os.getenv("PASSWORD")
# URL = os.getenv("URL")
# PORT = os.getenv("PORT")
# url = urljoin(f"http://{USER}:{PASSWORD}@{URL}:{PORT}", "video")
# capture = cv2.VideoCapture(url)
capture = cv2.VideoCapture(0) # you can change this parameter to another integer to get a different camera source


while(capture.isOpened()):
    ret, frame = capture.read()

    frame = rescale_frame(frame, percent=50)
    h, w, c = frame.shape

    if (cv2.waitKey(1) == ord("s")):
        break
    qrDetector = cv2.QRCodeDetector()
    data, bbox, rectifiedImage = qrDetector.detectAndDecode(frame)

    if len(data) > 0:
        print(f"Data: {data}")
        rectifiedImage = rescale_frame(rectifiedImage, percent=1000)
        cv2.imshow("QR Code", rectifiedImage)
        cv2.moveWindow("QR Code", w, 0)
    else:
        cv2.imshow("Webcam", frame)
        cv2.moveWindow("Webcam", 0, 0)

capture.release()
cv2.destroyAllWindows()