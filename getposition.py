import cv2
import numpy as np

def getpos(frame, lower_limit, upper_limit):
    x_res, y_res = 650, 500
    #Resize and coverting BGR to HSV
    frame = cv2.resize(frame, (x_res,y_res))
    #frame = cv2.flip(frame,1)
    #cv2.imshow('frame',frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _,lightThresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV)
    frame = cv2.bitwise_and(frame, frame, mask=lightThresh)
    blur = cv2.GaussianBlur(frame,(7,7),0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    #Finding the range in image
    out = cv2.inRange(hsv, lower_limit, upper_limit)
    dilated = cv2.dilate(out, cv2.getStructuringElement(cv2.MORPH_RECT,ksize=(7,7)))

    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  
    cx, cy = 0,0
    min_x, min_y = -10000,-10000 #OK?
    if len(contours) > 0:
        for _,cnt in enumerate(contours):            
            M = cv2.moments(cnt)
            if M['m00'] != 0:
                area = cv2.contourArea(cnt)
                if area>500:
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    if (cy > min_y): #OK?
                        min_x = cx
                        min_y = cy
    else:
        return (-10000, -10000)

    return (min_x,min_y)

def callme():
    frame = cv2.imread('image.png')
    #blue   
    lower_limit_blue = np.array([66,0,0])
    upper_limit_blue =  np.array([180,255,255])
    x_min_blue, y_min_blue = getpos(frame, lower_limit_blue, upper_limit_blue)

    #red
    lower_limit_red =   np.array([0,0,135])
    upper_limit_red =  np.array([0,255,255])
    x_min_red, y_min_red = getpos(frame, lower_limit_red, upper_limit_red)

    #green
    lower_limit_green =   np.array([15,0,0])
    upper_limit_green =  np.array([85,255,255])
    x_min_green, y_min_green = getpos(frame, lower_limit_green, upper_limit_green)

    if (y_min_blue >= y_min_red and y_min_blue >= y_min_green): return (x_min_blue,y_min_blue, 'b')
    elif (y_min_red >= y_min_blue and y_min_red >= y_min_green):  return (x_min_red,y_min_red, 'r')
    elif (y_min_green >= y_min_blue and y_min_green >= y_min_red):  return (x_min_green,y_min_green, 'g')
    else: return (-10000, -10000, '-10000')    
    # if (x_min_blue == 10000 and y_min_blue == 10000):
    #     return (x_min_red,y_min_red, 'r')
    # elif(x_min_red == 10000 and  y_min_red == 10000):
    #     return (x_min_blue,y_min_blue, 'b')
    # elif (y_min_blue <= y_min_red): return  (x_min_red,y_min_red, 'r')
    # elif (y_min_blue > y_min_red): return (x_min_blue,y_min_blue, 'b')
    # else: return (10000, 10000, '10000')

# print(callme())