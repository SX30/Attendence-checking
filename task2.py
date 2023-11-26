from keras.models import load_model  # TensorFlow is required for Keras to work
from PIL import Image, ImageOps  # Install pillow instead of PIL
import numpy as np
from Adafruit_IO import MQTTClient
import time
import cv2
cam = cv2.VideoCapture(0)

def image_capture():
    ret,frame = cam.read()
    cv2.imwrite ("test.png",frame)

# Disable scientific notation for clarity
np.set_printoptions(suppress=True)

# Load the model
model = load_model("keras_Model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()
data= np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

def image_detector():
    data= np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    # Replace this with the path to your image
    image = Image.open("test.png").convert("RGB")

    # resizing the image to be at least 224x224 and then cropping from the center
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)

    # turn the image into a numpy array
    image_array = np.asarray(image)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1

    # Load the image into the array
    data[0] = normalized_image_array

    # Predicts the model
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # Print prediction and confidence score
    print("Please stand before the camera: \n")
    print("Class:", class_name[2:], end="")
    print("Confidence Score:", confidence_score)

    #get the 1D array
    output = prediction[0]

    #assign default value for max confidence
    global max_index
    max_index = 0
    max_confidence = output[0]

    #find the maximum confidence and its index
    for i in range(1, len(output)):

        if max_confidence < output[i]:

            max_confidence = output[i]

            max_index = i

    print(max_index, max_confidence)
    file = open("labels.txt",encoding="utf8")
    data = file.read().split("\n")
    print("AI Result: ", data[max_index])
    client.publish("ai", data[max_index])
    return max_index

client = MQTTClient("SXthirty","aio_JcvZ08nwdyyvONy9xD5YTvCN7FwJ")
client.connect()
client.loop_background(1)
while True:
    time.sleep(30)
    image_capture()
    image_detector()
    break
