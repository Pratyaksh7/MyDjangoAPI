import cv2

image = cv2.imread("static/images/svg1.png")

while True:
 cv2.imshow("This is my Image",image)
 if cv2.waitKey(1) == ord("q"):
     break