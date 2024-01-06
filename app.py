import cv2, time 
import numpy as np

video = cv2.VideoCapture(0)

target_color = 	(255, 193, 204)
target_color_range = 5.0


#vid ref https://www.youtube.com/watch?v=oxmZ9zczptg&ab_channel=Iknowpython

first_frame = None
print("initalizing...")
#more accurate prediciton of position overtime

predictedPositionX = None
predictedPositionY = None

deltaWeight = .3
"""
Things to take in to consideration for confidence of object,
Color, how far away from a target color is the contour
Erraticness, how far away from the already predicted position is the contour

All the above?
"""

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

    avgXThisFrame = 0
    avgYThisFrame = 0
    avgCountThisFrame = 0
    #later create some sort of confidence scale to update the average, based on color


    for i, contour in enumerate(cntr):
#####
        avgCountThisFrame = i + 1
        mask = np.zeros_like(gray)
        cv2.drawContours(mask, [contour], 0, 255, -1)

        # Find the average color of the contour
        mean_color = cv2.mean(frame, mask=mask)[:3]

        # Print the average color of the contour
        #print(f"Contour {i+1} has an average color of BGR({mean_color[0]:.2f}, {mean_color[1]:.2f}, {mean_color[2]:.2f})")

        color_difference = np.subtract(target_color, mean_color)
        color_distance = np.linalg.norm(color_difference)
        #print(color_distance)

        # Check if the mean color is within the target color range
        within_range = np.all(np.abs(color_difference) <= target_color_range)
        if within_range:
            print("contour is in color range")
        # if cv2.contourArea(contour)<1000:
        #     continue
        (x,y,w,h)= cv2.boundingRect(contour)
        avgXThisFrame += x
        avgYThisFrame += y

        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),3)
    
    if avgCountThisFrame > 0:
        avgXThisFrame = avgXThisFrame / avgCountThisFrame
        avgYThisFrame = avgYThisFrame / avgCountThisFrame
        print(avgXThisFrame)
        print(avgYThisFrame)

        cv2.rectangle(frame, (int(avgXThisFrame), int(avgYThisFrame)), (int(avgXThisFrame) + 100, int(avgYThisFrame) + 100), (255, 0 , 0), 2)

        if predictedPositionX == None and predictedPositionY == None:
            predictedPositionX = avgXThisFrame
            predictedPositionY = avgYThisFrame
        else:
            deltaX = avgXThisFrame - predictedPositionX
            deltaY = avgYThisFrame - predictedPositionY
            predictedPositionX += deltaX * deltaWeight
            predictedPositionY += deltaY * deltaWeight
            print(predictedPositionX)
            print(predictedPositionY)


    if predictedPositionY and predictedPositionX:
        cv2.rectangle(frame, (int(predictedPositionX), int(predictedPositionY)), (int(predictedPositionX) + 100, int(predictedPositionY) + 100), (0, 0 , 255), 2)


    #cv2.imshow("capturing",gray)
    cv2.imshow("axolotlTime",frame)
    key=cv2.waitKey(1)
    if key==ord('q'):
        print("exiting")
        break

video.release()
cv2.destroyAllWindows()
