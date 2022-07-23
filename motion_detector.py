import cv2
from datetime import datetime
import pandas as pd

#A placeholder for the reference frame that will be used to diff from the current frame
reference_frame=None
#'None, None' = To escape 'IndexError' list index out of range
status_list=[None, None]
times=[]
a = 100

df = pd.DataFrame(columns=["Start", "End"])

#Captures the video from the camera
video=cv2.VideoCapture(0)

#Iterate through each frame received from the camera until 'q' keypress
while True:
    a += 1
    #Reads the frame into the values of check, and frame as a 3D array using BGR color format 
    check, frame = video.read()

    #a variable to denote there is no motion in the initial frame
    status=0

    #Convert frame to grayscale using BG22GRAY
    gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #This will blur the image so that the pixels are less accurate for simplicity
    gray=cv2.GaussianBlur(gray, (21,21), 0)

    #Sets the 3D array and image for the reference frame that will be used for diffing from the current frame
    if reference_frame is None:
        #sets the initial reference_frame when the value of reference_frame is None
        print("initial")
        reference_frame=gray
        continue
    elif a == 200:
        #Updates the reference frame after 200 iterations as to account for anything that might have been moved in the frame but then came to a stop
        reference_frame=gray
        continue

    #Finds the delta from the reference image and the current image
    delta_frame=cv2.absdiff(reference_frame, gray)

    #Applies thresholds to the frame if the difference between the initial frame and the current frame is less than 'threshold'
    #pixels then the threshold image will apply a 255 value in that index of the array signifying the color "white"
    threshold = 30
    thresh_frame=cv2.threshold(delta_frame, threshold, 255, cv2.THRESH_BINARY)[1]
    thresh_frame=cv2.dilate(thresh_frame, None, iterations=2)

    #Lists all the contours in the image, i.e. if you have 2 distinct sections where there are diff images than the initial image
    #then there will be two contours created for the separate sections
    (cnts,_) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #As to avoid the initial reference image that might be incorrect due to camera focus etc.
    if a >200:
        #Loops through all the contours that have been found in the threshold image
        for contour in cnts:
            #If the number of pixels in the contour is less than 2000 it ignores that contour
            #as to ignore any small changes like shadows etc.
            if cv2.contourArea(contour) < 5000:
                continue
            
            #using cv2.boundingRect gets the upper left corner x, y cordinates and the width/height of the contour
            (x, y, w, h)= cv2.boundingRect(contour)

            #If we do not continue out of the iteration of the for loop
            #'status' will update to 1 indicating that there is a change in the current image from reference frame
            status = 1
            #Applies a rectangle to the original frame using the 'color' provided for the boundary
            if w < 250 and h < 250:
                color=(0, 0, 255)
            else:
                color=(0, 255, 0)


            cv2.rectangle(frame, (x,y), (x+w, y+h), color, 3)

        #Creates a full list of the status of each iteration for calculating time and generating final graph
        status_list.append(status)

        #Determines if the status is changing in the status list
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())
        if status_list[-1] == 1 and status_list[-2] == 0:
            times.append(datetime.now())

    #Displays all 4 Frames to the screen
    cv2.imshow("Gray Frame", gray)
    cv2.imshow("Delta Frame", delta_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    #Waits 1 millisecond capturing if there is a key press
    key = cv2.waitKey(1)

    '''print(gray)
    print(delta_frame)
    print(thresh_frame)'''

    #Quits the while loop if keypress 'q'
    if key == ord('q'):
        if status == 1:
            #Ensures that if the application is closed while there is an object on the screen then the graph will 
            #display the object was on the screen from the time it entered until the time of quit
            times.append(datetime.now())
        break

#Prints the number of iterations of the while loop
print("Number of iterations" + str(a))

print(times)

#Steps through the times list and appends the time stamps to the data frame
#step of 2 so that : i = start times and i+1 = end times

for i in range(0, len(times), 2):
    df=df.append({"Start":times[i], "End":times[i+1]}, ignore_index=True)


df.to_csv("output/Times.csv")

video.release()

cv2.destroyAllWindows()