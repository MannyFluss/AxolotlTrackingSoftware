import cv2, time 

video = cv2.VideoCapture(0)

#vid ref https://www.youtube.com/watch?v=oxmZ9zczptg&ab_channel=Iknowpython

first_frame = None
print("initalizing...")
while True:
    check, frame = video.read()
    #grayscale for higher contrast
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray=cv2.GaussianBlur(gray,(21,21),0)
    #we store the first frame as a pivot for future objects of motion
    if first_frame is None:
        print("starting display.")
        first_frame = gray
        continue
    delta_frame = cv2.absdiff(first_frame,gray)
    threshold_frame = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
    threshold_frame = cv2.dilate(threshold_frame,None,iterations=3)

    (cntr,_)=cv2.findContours(threshold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in cntr:
        if cv2.contourArea(contour)<1000:
            continue
        (x,y,w,h)= cv2.boundingRect(contour)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    cv2.imshow("axolotlTime",frame)
    key=cv2.waitKey(1)
    if key==ord('q'):
        print("exiting")
        break

video.release()
cv2.destroyAllWindows()
