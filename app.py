import cv2
import numpy as np

def calculate_average_color(region):
    return np.mean(region, axis=(0, 1))

def is_color_close(color, target_color, threshold):
    return np.linalg.norm(color - target_color) < threshold

def process_frame(frame, target_color, target_color_range, chunk_size, show_chunks=False):
    height, width, _ = frame.shape
    positions = []
    
    for y in range(0, height, chunk_size):
        for x in range(0, width, chunk_size):
            region = frame[y:y+chunk_size, x:x+chunk_size]
            average_color = calculate_average_color(region)
            
            if is_color_close(average_color, target_color, target_color_range):
                center_position = (x + chunk_size // 2, y + chunk_size // 2)
                positions.append(center_position)
                
                if show_chunks:
                    # Draw a rectangle around the chunk
                    cv2.rectangle(frame, (x, y), (x + chunk_size, y + chunk_size), (0, 255, 0), 2)
    
    if positions:
        average_position = np.mean(positions, axis=0)
        if show_chunks:
            # Draw a circle at the average position
            cv2.circle(frame, (int(average_position[0]), int(average_position[1])), 10, (0, 0, 255), -1)
    else:
        average_position = None
    
    return average_position

video = cv2.VideoCapture(0)
target_color = np.array([42,23,206])
target_color_range = 50
chunk_size = 10
show_chunks = True  # Set this to True to show the chunks, False to hide them

# the predicted position
currPositionX = None
currPositionY = None

delta = .1

while True:
    check, frame = video.read()

    if not check:
        break

    frame = cv2.GaussianBlur(frame, (21, 21), 0)
    position = process_frame(frame, target_color, target_color_range, chunk_size, show_chunks)
    

    if position is not None:
        #initialize position
        if currPositionY == None:
            currPositionX = position[0]
            currPositionY = position[1]
        currPositionX += (position[0] - currPositionX) * delta
        currPositionY += (position[1] - currPositionY) * delta
        cv2.circle(frame, (int(currPositionX), int(currPositionY)), 10, (0, 255, 0), -1)


        #need to go back to get the areas stuff    
        for area in areas:
            area.poll_position(currPositionX,currPositionY)
            cv2.rectangle(frame, (area.areaDetector.x, area.areaDetector.y), 
                        (area.areaDetector.x + area.areaDetector.width, area.areaDetector.y + area.areaDetector.height), (0, 255, 255), 2)


    cv2.imshow("Axolotl Detection", frame)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        print("Exiting")
        break

video.release()
cv2.destroyAllWindows()

'''


'''
