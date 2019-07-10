# import the necessary packages
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to trained model model")
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

# load the image
image = cv2.imread(args["image"])

print("[INFO] loading network...")
model = load_model(args["model"])

orig = image.copy()

# pre-process the image for classification
image = cv2.resize(image, (128, 128))
image = image.astype("float") / 255.0  # handling scaling our image to the range [0, 1]
image = img_to_array(image)  # converting it to an array, and addding an extra dimension
image = np.expand_dims(image, axis=0)  # np.expand_dims  allows our image to have the shape (1, width, height, 3)
# load the trained convolutional neural network

label_List = list()
prob_List = []
# classify the input image
# (Mac, Other_Laptop, no_Laptop) = model.predict(image)[0]
label_List = model.predict(image)[0]
proba = np.amax(label_List)
max_Index = np.argmax(label_List, axis=None, out=None)
label_name = ['Mac', 'Other_Laptop', 'no_Laptop']
print(label_name[max_Index], proba)

# build the label
# label = "Other_Laptop" if Other_Laptop > Mac else "Mac"

# proba = Other_Laptop if Other_Laptop > Mac else Mac

label = '{}: {}% '.format(label_name[max_Index], label_List[max_Index] * 100)


# draw the label on the image
output = imutils.resize(orig, width=800)
cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

# show the output image
cv2.imshow("Output", output)
cv2.waitKey(0)
