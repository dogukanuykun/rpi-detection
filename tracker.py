import cv2, imutils
import time 
from RpiMotorLib import RpiMotorLib

#define GPIO pins
x_GPIO_pins = (14, 15, 18) # Microstep Resolution MS1-MS3 -> GPIO Pin
x_direction= 20       # Direction -> GPIO Pin
x_step = 21      # Step -> GPIO Pin

y_GPIO_pins = (22,27,17)
y_direction = 23
y_step = 24


# Declare an named instance of class pass GPIO pins numbers
motor_x = RpiMotorLib.A4988Nema(x_direction, x_step, x_GPIO_pins, "A4988")
motor_y = RpiMotorLib.A4988Nema(y_direction, y_step, y_GPIO_pins, "A4988")


csrt_tracker = cv2.TrackerCSRT_create()
video = cv2.VideoCapture(0)

_, frame = video.read()
frame = imutils.resize(frame, width=540)
BB = cv2.selectROI(frame, True)
csrt_tracker.init(frame, BB)
x_max, y_max = 720, 540

while True:
    _, frame = video.read()
    #print(frame.shape)
    frame = imutils.resize(frame, width=720)
    track_success, BB = csrt_tracker.update(frame)
    x1, y1, x2, y2 = BB
    distance_x = x1 - x_max//2
    distance_y = y1 - y_max//2
    #print(distance_y)
    #print(distance_y)
    if track_success:
        bottom_right = (int(BB[0] + BB[2]), int(BB[1] + BB[3]))
        top_left = (int(BB[0]), int(BB[1]))
        cv2.rectangle(frame, top_left, bottom_right, (0, 255, 0), 5)
        if(distance_x  > 75):
            motor_x.motor_go(True, "Full" , 10,.0005, False, .05) # x-axis clockwise turn
            continue
        elif(distance_x < -150):
            motor_x.motor_go(False, "Full" , 10,.0005, False, .05) # x-axis anticlockwise turn
            continue
        if(distance_y  > 20):
            motor_y.motor_go(True, "Full" , 10,.0005, False, .05)
            continue
        elif(distance_y < -200):
            motor_y.motor_go(False, "Full" , 10,.0005, False, .05)
            continue
    cv2.imshow('Output', frame)
    key = cv2.waitKey(1) & 0xff
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()




