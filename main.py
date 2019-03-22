import requests
import cv2
from cv2 import *
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
# import matplotlib.pyplot as plt
# import image
# from io import BytesIO



# IMAGE CAPTURE: initialize the camera
i = 0
cam = VideoCapture(0)   # 0 -> index of camera
s, img = cam.read()
if s:    # frame captured without any errors
    namedWindow("cam-test", WINDOW_AUTOSIZE)
    imshow("cam-test",img)
    destroyWindow("cam-test")
    i += 1
    imwrite(f'filename{i}.jpg',img) #save image


# Replace <Subscription Key> with your valid subscription key.
subscription_key = "576a3dc3383c46b18d615f89184dd489"
assert subscription_key

# You must use the same region in your REST call as you used to get your
# subscription keys. For example, if you got your subscription keys from
# westus, replace "westcentralus" in the URI below with "westus".
#
# Free trial subscription keys are generated in the "westus" region.
# If you use a free trial subscription key, you shouldn't need to change
# this region.
vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

analyze_url = vision_base_url + "analyze"

# Set image_path to the local path of an image that you want to analyze.
image_path = f"C:/Users/mkear/PycharmProjects/object_detection_azure/filename{i}.jpg"

# Read the image into a byte array
image_data = open(image_path, "rb").read()
headers    = {'Ocp-Apim-Subscription-Key': subscription_key,
              'Content-Type': 'application/octet-stream'}
# params     = {'visualFeatures': 'Objects,Description,Color'}
params     = {'visualFeatures': 'Objects'}
response = requests.post(
    analyze_url, headers=headers, params=params, data=image_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'description' property.
analysis = response.json()
print(analysis)

image = cv2.imread(f"C:/Users/mkear/PycharmProjects/object_detection_azure/filename{i}.jpg")

found_objects = analysis['objects']
print(found_objects)
for i in range(len(found_objects)):
    rectangle = found_objects[i]['rectangle']
    x_min = rectangle['x']
    y_min = rectangle['y']
    x_max = rectangle['w']+x_min
    y_max = rectangle['h']+y_min
    cv2.rectangle(image,(x_min,y_min),(x_max,y_max),(0,255,0),2) # add rectangle to image
cv2.imshow('image', image)
cv2.waitKey(0)


# image_caption = analysis["objects"]["captions"][0]["text"].capitalize()
#
# # Display the image and overlay it with the caption.
# image = image.open(BytesIO(image_data))
# plt.imshow(image)
# plt.axis("off")
# _ = plt.title(image_caption, size="x-large", y=-0.1)