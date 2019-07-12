from django.shortcuts import render, redirect
from django.http import HttpResponse
import jsonpickle
import os
from keras.preprocessing.image import img_to_array
from keras.models import load_model
from keras import backend as K
import numpy as np
from django.shortcuts import render, redirect
from .forms import *
import cv2
from django.views.decorators.csrf import ensure_csrf_cookie
import datetime
import pickle
from gettingstarted.settings import BASE_DIR
import json
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
import base64
import io
from PIL import Image
from .forms import imageForm


@api_view(['POST', 'GET'])
def index(request):

    if request.method == "GET":
        return_data = {
            "error": "0",
            "message": "Laptop Classification for Search.By.Search"
        }
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        response = {}
        if form.is_valid():
            #  form.save()
            print('correct uptill now')
            image = cv2.imdecode(np.fromstring(request.FILES['Laptop_Img'].file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
            # header, image_data = request_data.split(';base64,')
            # nparr = np.fromstring(request_data, np.uint8)
            # for image in os.listdir('D:/Sofit_Deliverables/image-search-python/media/images/'):
            try:
                # image = 'D:/Sofit_Deliverables/image-search-python/media/images/Inkedimages_LI.jpg'
                print(image)
                # image = cv2.imread(image)
                # image = Image.open(io.BytesIO(base64.b64decode(image_data)))
                # default_image_size = tuple((128, 128))

                if image is not None:
                    image = cv2.resize(image, (128, 128))
                    image = image.astype("float") / 255.0  # handling scaling our image to the range [0, 1]
                    image = img_to_array(image)  # converting it to an array, and addding an extra dimension
                    image = np.expand_dims(image, axis=0)
                else:
                    print(None, "Error loading image file")

                print("[INFO] loading network...")
                print(BASE_DIR + "/hello/laptop_model.h5")
                #print(os.path.join(BASE_DIR, '/hello/laptop_model.h5'))
                model = load_model(BASE_DIR + "/hello/laptop_model.h5")

                # orig = image.copy()

                # pre-process the image for classification
                # image = cv2.resize(image, (128, 128))
                # image = image.astype("float") / 255.0  # handling scaling our image to the range [0, 1]
                # image = img_to_array(image)  # converting it to an array, and addding an extra dimension
                # image = np.expand_dims(image, axis=0)  # np.expand_dims  allows our image to have the shape (1, width, height, 3)
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
                        response_message += "Image contains: " + label_name[counter] + " with highest probability "
                    counter = counter + 1

                #  print('Other Details: \n')
                response_message += ' Details: '

                for key, val in final_list.items():
                    #  print(key + ': ', val, '\n')
                    response_message += ' ' + str(key) + ': ' + str(val) + ' '

                response = {}
                response['message'] = response_message
                print(response)
                # encode response using jsonpickle
                # return_data = jsonpickle.encode(response)
                # K.backend.clear_session()
                return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')
            except Exception as e:
                response = {
                    "error": "3",
                    "message": f"Error : {str(e)}",
                }
        # return HttpResponse(json.dumps(response), content_type='application/json; charset=utf-8')
        # form = imageForm()
        # return render(request, 'index.html', {'form': form})
        #  return redirect('success')
    else:
        form = imageForm()
    return render(request, 'index.html', {'form': form})


def success(request):
    return HttpResponse('successfuly uploaded')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, "db.html", {"greetings": greetings})
