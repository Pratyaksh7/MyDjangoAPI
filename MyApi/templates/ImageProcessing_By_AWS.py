import boto3
import requests
import cv2


def ObjectDetection(imagePath, Service):
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
                MyImage = cv2.putText(MyImage, objectName, (x, y-20), cv2.FONT_HERSHEY_COMPLEX,1, (0,0,255),1)

    cv2.imwrite("detected.jpg", MyImage)

ObjectDetection("C:/Users/Pratyaksh/Desktop/IMG_20190129_105707.jpg","Object detection")
