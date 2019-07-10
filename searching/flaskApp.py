#  import the necessary packages

from flask import Flask, request, Response
import jsonpickle
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import numpy as np
import argparse
import imutils
import cv2


# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/test', methods=['POST'])
# construct the argument parse and parse the arguments
def test():
    # ap = argparse.ArgumentParser()
    # # ap.add_argument("-m", "--model", required=True, help="path to trained model model")
    # ap.add_argument("-i", "--image", required=True, help="path to input image")
    # args = vars(ap.parse_args())

    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)

    # load the image
    #  image = cv2.imread(args["image"])

    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print("[INFO] loading network...")
    model = load_model('D:/Sofit_Deliverables/SearchByImage/laptop_model.h5')

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
    counter = 0
    label_List = model.predict(image)[0]
    label_name = ['Mac', 'Laptop', 'no_Laptop']
    final_list = {}

    response_message = ''

    for prob in label_List:
        prob = round(prob * 100, 2)
        final_list[label_name[counter]] = prob
        if(prob >= 70):
            #  print("Image contains: " + label_name[counter] + " with highest probability \n")
            response_message += "Image contains: " + label_name[counter] + " with highest probability \n"
        counter = counter + 1

    #  print('Other Details: \n')
    response_message += ' Details: \n'

    for key, val in final_list.items():
        #  print(key + ': ', val, '\n')
        response_message += ' ' + str(key) + ': ' + str(val) + ' \n'

    # build a response dict to send back to client
    # response = {'message': 'image received. size={}x{} \n {}'.format(image.shape[1], image.shape[0], response_message)}
    response = {'Response: ': ' \n ' + response_message}
    _, img_encoded = cv2.imencode('.jpg', orig)
    # response = {'data': img_encoded, content_type = 'image/jpeg'}
    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

    #  proba = np.amax(label_List)
    #  max_Index = np.argmax(label_List, axis=None, out=None)
    #  label_name = ['Mac', 'Laptop', 'no_Laptop']

    #  print(label_name[max_Index], proba)

    # build the label
    # label = "Other_Laptop" if Other_Laptop > Mac else "Mac"

    # proba = Other_Laptop if Other_Laptop > Mac else Mac

    #  label = '{}: {}% '.format(label_name[max_Index], label_List[max_Index] * 100)
    #  label = '{}:'.format(label_name[max_Index])

    # draw the label on the image
    #  output = imutils.resize(orig, width=800)
    #  cv2.putText(output, label, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    # show the output image
    #  cv2.imshow("Output", output)
    #  cv2.waitKey(0)


# start flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='6000', debug=True)
