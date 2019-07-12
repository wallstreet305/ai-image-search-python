from __future__ import print_function
import requests
import json
import numpy as np
import cv2

addr = 'http://localhost:8000'
test_url = addr

# prepare headers for http request
content_type = 'image/jpeg'
headers = {'content-type': content_type}

img = cv2.imread('D:/Sofit_Deliverables/SearchByImage/Mac00004.png')
# encode image as jpeg
_, img_encoded = cv2.imencode('.jpg', img)
# send http request with image and receive response
response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

# nparr = np.fromstring(response.text, np.uint8)
# load the image

# image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
# cv2.imshow('image', image)
# decode response
print(json.loads(response.text))