from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from .models import MyFile


import boto3
import requests
import cv2

# django rest api modules
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, parser_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import MultiPartParser, FormParser

def ObjectDetection(imagePath):
    session = boto3.Session(profile_name="default")
    Service = session.client("rekognition")
    image = open(imagePath,"rb").read()
    imgH, imgW = cv2.imread(imagePath).shape[:2]
    MyImage = cv2.imread(imagePath)
    response = Service.detect_labels(Image = {"Bytes": image})
    for objects in response["Labels"]:
        if objects["Instances"]:
            objectName = objects["Name"]
            for boxs in objects["Instances"]:
                box = boxs["BoundingBox"]
                x = int(imgW * box["Left"])
                y = int(imgH * box["Top"])
                w = int(imgW * box["Width"])
                h = int(imgH * box["Height"])

                MyImage = cv2.rectangle(MyImage, (x,y), (x+w, y+h), (0,255,0), 2)
                MyImage = cv2.putText(MyImage, objectName, (x, y), cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255),1)
    cv2.imwrite(imagePath, MyImage)



def Celebrities_Detection(imagePath):
    session = boto3.Session(profile_name="default")
    Service = session.client("rekognition")
    image = open(imagePath,"rb").read()
    imgH, imgW = cv2.imread(imagePath).shape[:2]
    MyImage = cv2.imread(imagePath)
    response = Service.recognize_celebrities(Image = {"Bytes": image})
    for objects in response["CelebrityFaces"]:
        CelName = objects["Name"]
        Face = objects["Face"]
        box = Face["BoundingBox"]
        x = int(imgW * box["Left"])
        y = int(imgH * box["Top"])
        w = int(imgW * box["Width"])
        h = int(imgH * box["Height"])

        MyImage = cv2.rectangle(MyImage, (x,y), (x+w, y+h), (0,255,0), 2)
        MyImage = cv2.putText(MyImage, CelName, (x, y), cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255),1)

    cv2.imwrite(imagePath, MyImage)


@api_view(["GET", "POST"])
@renderer_classes([JSONRenderer]) # produce result in this format -> {"Url":"http://127.0.0.1:8000/MEDIA/IMG_20190331_145856.jpg"}
@parser_classes([MultiPartParser,FormParser])
def index(request):
    if request.method == "POST":
        img = request.FILES['image']
        service = request.POST["service"]
        data = MyFile.objects.create(image = img)   # image is the column name in the table(Model) in database
        path = str(settings.MEDIA_ROOT) + "/" + data.image.name
        # print(path)
        if service == "Object Detection":
            ObjectDetection(path)

        if service == "Celeb Detect.":
            Celebrities_Detection(path)

        url = "http://127.0.0.1:8000" + data.image.url
        Msg = {"Url":url}
        return Response(data = Msg, status = status.HTTP_200_OK)

    return render(request, "index.html")


######  WORK with API ######



