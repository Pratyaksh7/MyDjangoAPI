import cv2

image = cv2.imread("static/images/svg1.png")

text = "Pratyaksh"
text_image = cv2.putText(image, text, (0,30), cv2.FONT_HERSHEY_COMPLEX,1, (255,0,0),1)
text_box_image = cv2.rectangle(text_image,(30,30),(200,200),(0,255,0),2)

while True:
    cv2.imshow("Default Image", text_box_image)
    if cv2.waitKey(0) == ord('q'):
        # cv2.destroyAllWindows()
        break