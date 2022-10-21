import PySimpleGUI as sg # GUI Manager.
import numpy as np
import cv2 


canvas_size = (500, 800) # [px]


coord_size = (2160, 3800)

step_size = 15

window_size = (480, 800) # [px]


# Define layout for window.
layout = [[sg.Graph(canvas_size, (0, 0), coord_size,
                    background_color = "grey5", k="-MAP-")]]


# Init. Window.
window = sg.Window("Quantifying Chaos", layout,
                   background_color="grey15",
                   finalize=True,
                   margins=(10, 10))


green = 60
blue = 120
yellow = 30


cap = cv2.VideoCapture("footage/C0155.MP4")

"""
while True:

    _, frame = cap.read()

    frame = cv2.rotate(frame, cv2.ROTATE_180)

    frame = frame[200:2700, 00:3000] # Crop, y_upper:ylower, x_left:x_right [px]

    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    

    # define range of white color in HSV
    sensitivity = 180

    colour = blue

    lower_bound = 99
    
    lower_colour = np.array([colour - sensitivity, lower_bound, lower_bound]) 
    upper_colour = np.array([colour + sensitivity, 255, 255])


    # Threshold the HSV image to get only white colors
    mask = cv2.inRange(hsv, lower_colour, upper_colour)
    
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)

    for win in ['res', 'mask', 'frame']:
        cv2.namedWindow(win, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(win, window_size[0], window_size[1])

    
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)

    cv2.imshow('frame',frame)
    

    k = cv2.waitKey(5) & 0xFF
    
    if k == 27:
        break

cv2.destroyAllWindows()
"""
"""
while 1:
    ret,frame =cap.read()

    frame = cv2.rotate(frame, cv2.ROTATE_180)

    frame = frame[200:2700, 00:3000] # Crop, y_upper:ylower, x_left:x_right [px]


    # ret will return a true value if the frame exists otherwise False
    into_hsv =cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    # changing the color format from BGr to HSV
    # This will be used to create the mask
    
    L_limit=np.array([15,15,15]) # setting the blue lower limit
    U_limit=np.array([200,255,255]) # setting the blue upper limit
        
 
    b_mask=cv2.inRange(into_hsv,L_limit,U_limit)
    # creating the mask using inRange() function
    # this will produce an image where the color of the objects
    # falling in the range will turn white and rest will be black
    blue=cv2.bitwise_and(frame,frame,mask=b_mask)
    # this will give the color to mask.

    for win in ['res']:
        cv2.namedWindow(win, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(win, window_size[0], window_size[1])
        
    #cv2.imshow('frame',frame) # to display the original frame
    cv2.imshow('res',blue) # to display the blue object output
 
    if cv2.waitKey(1)==27:
        break
    # this function will be triggered when the ESC key is pressed
    # and the while loop will terminate and so will the program
cap.release()
"""

def rgb2hex(rgb):

    return '#%02x%02x%02x' % rgb



n = -1
while True:

    n += 1

    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED:
        window.close()
        break;

    ret, frame = cap.read()

    if (n % 20) != 0:
        continue

    #frame = cv2.rotate(frame, cv2.ROTATE_180)

    

    #frame = frame[200:2700, 00:3000] # Crop, y_upper:ylower, x_left:x_right [px]

    #for win in ['frame']:
    #    cv2.namedWindow(win, cv2.WINDOW_NORMAL)
    #    cv2.resizeWindow(win, window_size[0], window_size[1])
        
    #cv2.imshow('frame',frame) # to display the original frame

    #window["-MAP-"].draw_point((1, 1), size = 20, color="red")

    for i in range(250, 3500, step_size):
        for j in range(150, 2100, step_size):

            #print(i, j)

            col = rgb2hex((int(frame[i, j][0]),
                           int(frame[i, j][1]),
                           int(frame[i, j][2])))

            window["-MAP-"].draw_point((j, i), size = 32, color = col)

            window.refresh()

    print(".", end="")

    
            
        
