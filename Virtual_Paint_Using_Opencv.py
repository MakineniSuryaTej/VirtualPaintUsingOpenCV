import cv2
import numpy as np

frameWidth, frameHeight = 640, 480
cap = cv2.VideoCapture(1)  # Parameter 1 is for webcam && 0 is for Integrated Camera
cap.set(3, frameWidth)  # Adjusting Width of Output Window
cap.set(4, frameHeight)  # Adjusting Height of Output Window
cap.set(10, 150)  # Adjusting the Brightness ot Output Window

# If we want to Add new colors add the values to the below list
myColors = [[25, 23, 0, 165, 255, 255],  # Blue Color values for detection
            [10, 93, 0, 90, 250, 255],  # Yellow Color values for detection
            [116, 35, 102, 179, 255, 255],  # Pink Color values for detection
            [0, 106, 99, 7, 255, 255]  # Orange Color values for detection
            ]
myColorValues = [[255, 204, 0],  # BGR value of Blue
                 [0, 255, 255],  # BGR value of Yellow
                 [204, 102, 255],  # BGR value of Pink
                 [0, 102, 255]  # BGR value of Orange
                 ]
myPoints = []  # Initialising the points list for drawing


def findColor(img, myColors, myColorValues):  # Function for finding colors in the Camera or Webcam
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    counter = 0
    newPoints = []  # List consists of Circle centre points and color value
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)  # Creating the mask
        x, y = getContours(mask)  # Calling the Function for getting the centre of the circle
        cv2.circle(imgResult, (x,y), 10, myColorValues[counter], cv2.FILLED)  # Fixed circle at the top of the contour
        if x != 0 and y != 0:  # if both x and y are 0's there is no need to add them to new points
            newPoints.append([x, y, counter])
        counter += 1
    return newPoints  # Returning the points


def getContours(img):  # Functions for drawing contours
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)  # Finding Contours
    x, y, w, h = 0, 0, 0, 0  # Initialising the centre, width and height
    for cnt in contours:
        area = cv2.contourArea(cnt)  # Finding area of the detected contour
        if area > 500:
            cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)  # Drawing the border for detected Contour
            perimeter = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            x, y, w, h = cv2.boundingRect(approx)  # Retrieving boundaries
    return x+w//2, y  # Returns the top point of contour for the


def drawArt(myPoints, myColorValues):  # This function draws on the Window for every point it detects
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 17, myColorValues[point[2]], cv2.FILLED)  # Drawing Circles


while True:  # Infinite Loop since we are using a Camera or WebCam
    success, img = cap.read()
    imgResult = img.copy()  # Final Required Result
    newPoints = findColor(img, myColors, myColorValues)  # Retrieving the Points List
    if len(newPoints) != 0:
        for new in newPoints:  # Appending all the new points to the List which are to be drawn
            myPoints.append(new)
    if len(myPoints) != 0:
        drawArt(myPoints, myColorValues)  # Calling this function to draw circles on the Window
    cv2.imshow("Result", imgResult)  # Displaying the Window
    if cv2.waitKey(1) & 0xFF == ord('q'):  # By pressing the 'q' key on keyboard the execution will be terminated
        break
