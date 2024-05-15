#Importing Libraries
import base64
import json
import time
from django.shortcuts import render
from channels.db import database_sync_to_async
from .models import Suspect

import cv2 as cv
import numpy as np
import os
import asyncio
import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
import pickle
from keras_facenet import FaceNet
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
import threading

import cloudinary
import cloudinary.uploader
import cloudinary.api


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#Initializing AI Models
facenet = FaceNet()
faces_embeddings = np.load(DIR + '/camerafeatures/AImodels/EmbeddingFaces-MiriamNermine-Draft1.npz')
Y = faces_embeddings['arr_1']
encoder = LabelEncoder()
encoder.fit(Y)
haarcascade = cv.CascadeClassifier(DIR +'/camerafeatures/AImodels/haarcascade_frontalface_default.xml')
model = pickle.load(open(DIR +'/camerafeatures/AImodels/FaceDetectionModel-Draft1.pkl', 'rb'))


#Initialize Cloudinary
cloudinary.config(
    cloud_name="dj7g2kilb",
    api_key="965337921533992",
    api_secret="hGGNwe2vPTNMHRb216mj7xlqrAU"
)

#FaceRecognition WebSocket Connection

class FaceRecg(AsyncWebsocketConsumer):
    global final_name
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.loop = asyncio.get_event_loop()
        self.groupname = "FaceRecognition"

    async def connect(self):
        # Initialization code when a WebSocket connection is established
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        print(self.groupname)
        print(self.channel_name)
        await self.accept()
        print("WebSocket FaceRecognition connection established")


    async def disconnect(self, close_code):
        print("WebSocket FaceRecognition connection disconnected")
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        raise StopConsumer()

    async def receive(self, bytes_data):
        # Function executed when the server receives data from the client

        if not (bytes_data):
            self.i = 0
            self.fps = 0
            self.prev = 0
            self.new = 0
            print('Closed connection')
            await self.close()
        else:
            self.frame = await self.loop.run_in_executor(None, cv.imdecode, np.frombuffer(bytes_data, dtype=np.uint8), cv.IMREAD_COLOR)
            self.rgb_img = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
            self.gray_img = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)

            faces = haarcascade.detectMultiScale(self.gray_img, 1.3, 5)
            Suspectname = []
            suspectdatalist=[]

            print("Suspect(s) Found: ")
            i=0
            for self.x, self.y, self.w, self.h in faces:
                self.img = self.rgb_img[self.y:self.y + self.h, self.x:self.x + self.w]
                self.img = cv.resize(self.img, (160, 160))  # 1x160x160x3
                self.img = np.expand_dims(self.img, axis=0)
                self.ypred = facenet.embeddings(self.img)
                self.face_name = model.predict(self.ypred)
                self.yhat_prob = model.predict_proba(self.ypred)
                self.class_index = self.face_name[0]
                self.class_probability = self.yhat_prob[0, self.class_index] * 100
                cv.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 255), 10)
                if self.class_probability > 80:
                    Suspectname.append(encoder.inverse_transform(self.face_name)[0])
                    print(Suspectname[i], end=" ")
                    suspectdatalist = await database_sync_to_async(self.getsuspectdata)(Suspectname)
                    cv.rectangle(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 0, 255), 10)
                    cv.putText(self.frame, str(Suspectname[i]) + " " + str(self.class_probability), (self.x, self.y - 10), cv.FONT_HERSHEY_SIMPLEX,
                               1, (0, 0, 255), 3, cv.LINE_AA)
                    i = i + 1

            self.buffer_img = await self.loop.run_in_executor(None, cv.imencode, '.jpeg', self.frame)
            self.b64_img = base64.b64encode(self.buffer_img[1]).decode('utf-8')
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'sendresult',  # function name to run
                    'frame': self.b64_img,  # value to send function
                    'suspectlist': Suspectname ,
                    'suspectdatalist': suspectdatalist,
                }
            )
            print(Suspectname)

    async def sendresult(self, event):
        frame = event['frame']
        suspectlist=event['suspectlist']
        suspectdatalist = event['suspectdatalist']
        # Send the message to the WebSocket
        await self.send(text_data=json.dumps(
            {
                'frame':frame,
                "suspectlist":suspectlist,
                "suspectdatalist": suspectdatalist,
            }))

    def getsuspectdata(self,suspectlist):
        suspectdata = []
        for suspect in suspectlist:
            suspect = suspect[:-1]
            data= Suspect.objects.filter(First_name=suspect).values()
            datadict = list(data)
            suspectdata.append(datadict[0])
            return suspectdata



#LiveStreaming WebSocket Connection
class livestreaming(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.loop = asyncio.get_event_loop()
        self.groupname = "LiveStreaming"

    async def connect(self):
        # Initialization code when a WebSocket connection is established
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )
        print(self.groupname)
        print(self.channel_name)
        await self.accept()
        print("WebSocket FaceRecognition connection established")

    async def disconnect(self, close_code):
        print("WebSocket FaceRecognition connection disconnected")
        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        raise StopConsumer()

    async def receive(self, text_data=None, bytes_data=None):
        if not (bytes_data):
            self.i = 0
            self.fps = 0
            self.prev = 0
            self.new = 0
            print('WebSocket FaceRecognition connection disconnected')
            await self.close()
        else:
            self.frame = await self.loop.run_in_executor(None, cv.imdecode, np.frombuffer(bytes_data, dtype=np.uint8), cv.IMREAD_COLOR)
            self.rgb_img = cv.cvtColor(self.frame, cv.COLOR_BGR2RGB)
            self.gray_img = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)


            # Encode frame as JPEG and convert to base64
            self.buffer_img = await self.loop.run_in_executor(None, cv.imencode, '.jpeg', self.frame)
            self.b64_img = base64.b64encode(self.buffer_img[1]).decode('utf-8')

            # Broadcast the base64-encoded image to all connected clients
            await self.channel_layer.group_send(
                self.groupname,
                {
                    'type': 'send_frame',
                    'frame': self.b64_img
                }
            )

    async def send_frame(self, event):
        frame = event['frame']
        await self.send(frame)


#Getting all pics from cloudinary
def getcloudinarypics(request):
    response = cloudinary.api.resources(type='upload' , prefix= 'R4ID/', max_results=50)
    cloudinary_image_urls = [item['secure_url'] for item in response['resources']]
    initial_image = cloudinary_image_urls[0] if cloudinary_image_urls else ''
    #render(request, 'Captureimage.js',{'cloudinary_image_urls': cloudinary_image_urls, 'initial_image': initial_image})
    return render(request, 'CaptureImage.html',{'cloudinary_image_urls': cloudinary_image_urls, 'initial_image': initial_image})


#Rendering to HTML Files

def FaceRecgrender(request):
    return render(request, 'Facereg.html')

def Livestreamingrender(request):
    return render(request, 'LiveStreaming.html')
