import pygame # Load the Pygame library to work with a gamepad
import time  #  Load the time library for time based commands
from time import sleep  #  Load the sleep command from the time library to allow for delays
from gpiozero import LED  #  Load the LED function from the gpiozero library for access to the Remote GPIO
from gpiozero import PWMLED #  Load the PWMLED function from the gpiozero library for access to the Remote GPIO
from gpiozero import Button  #  Load the Button function from the gpiozero library for access to the Remote GPIO
from gpiozero import Servo  #  Load the Servo function from the gpiozero library for access to the Remote GPIO
from gpiozero.pins.pigpio import PiGPIOFactory  #  Load the PiPIOFactory library to use Remote GPIO

factory = PiGPIOFactory(host='192.168.0.202')  #  Establish a networked connection to a Remote GPIO on IP Address 192.168.0.202

UpCam = LED(13, pin_factory=factory)  #  Set UpCam as in LED pin 13 for control of the camera relay to switch between the up and down cameras
LeftHorizontal = Servo(20, pin_factory=factory)  #  Set LeftHorizontal as a Servo on pin 20
RightHorizontal = Servo(21, pin_factory=factory)  # Set RightHorizontal as a Servo on pin 21
Left45 = Servo(19, pin_factory=factory)  #  Set Left45 as a Servo on pin 19
Right45 = Servo(26, pin_factory=factory)  #  Set Right45 as a Servo on pin 26
twist = Servo(5, pin_factory=factory)  #  Set twist as a Servo on pin 5 for the arm which we were unsuccessful at properly waterproofing
hand = Servo(6, pin_factory=factory)  #  Set hand as a Servo on pin 6 for the arm which we were unsuccessful at properly waterproofing
cam = 0  #  Set default camera value to 0 so the bottom camera will be turned on.
claw = 0.00  #  Set the claw default value to Zero for it's home position
arm = 0.00  #  Set the arm default value to Zero for it's home position

pygame.joystick.init()  #  Initialize the pygame joystick interface
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]  # Search for all joysticks and assign them each a number
print(joysticks)  #  Print the joysticks found
pygame.init()  # Initialize the pygame interface
direction = int  # Set a variable for the joystick axis direction as an integer. Values we will be looking for are 0, 1, 2, 3.  Left stick = 0 & 1.  Right stick = 2 & 3.
power = float(0.00)  # Set a float variable for the power we will be reading from the joystick axis's.
pwm = float(0.00)  # Set a float variable for the pwm values we will be outputting to the ESC's.

def left_forward():  #  Left horizontal forward function
    pwm = abs(power)   # Take the absolute value of the power function coming from the joystick axis and assign it to pwm  
    LeftHorizontal.value=-pwm  #  Send a negative pwm value to the left horizontal esc
    
def left_reverse():  #  Left horizontal reverse function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    LeftHorizontal.value=pwm  #  Send a positive pwm value to the left horizontal esc

def left_forward_reverse_stop():  # Left horizontal stop function
    LeftHorizontal.value=0  # Send a full stop pwm value to the left horizontal esc

def left_up():  # Left vertical up function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    Left45.value=pwm  #  Send a positive pwm value to the left vertical esc
    
def left_down():  # Left vertical down function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    Left45.value=-pwm  #  Send a negative pwm value to the left vertical esc

def left_up_down_stop():  # Left vertical stop function
    Left45.value=0  # Send a full stop pwm value to the left vertical esc
    
def right_forward():  # Right horizontal forward function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    RightHorizontal.value=pwm  #  Send a positive pwm value to the right horizontal esc
      
def right_reverse():  # Right horizontal reverse function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    RightHorizontal.value=-pwm  #  Send a negative pwm value to the right horizontal esc
    
def right_forward_reverse_stop():  #  Right horizontal stop function
    RightHorizontal.value=0  #  Send a full stop pwm value to the right horizontal esc

def right_up():  # Right vertical up function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    Right45.value=-pwm  #  Send a negative pwm value to the right vertical esc
    
def right_down():  #  Right vertical down function
    pwm = abs(power)  # Take the absolute value of the power function coming from the joystick axis and assign it to pwm 
    Right45.value=pwm  # Send a positive pwm value to the right vertical esc
     
def right_up_down_stop():  # Right vertical stop function
    Right45.value=0  #  Send a full stop pwm value to the right vertical esc

def blue():  # Extra blue joystick button not used
    print('Blue')  #  print on screen "Blue"
    
def green():  # Extra green joystick button not used
    print('Green')  #  print on screen "Green"
    
def orange():  # Extra orange joystick button not used
    print('Orange')  #  print on screen "Orange"
    
def red_stop():  #  Emergency Stop Setup on Red Button to stop all motors.  This was setup for the initial testing of the esc's, in case a motor got stuck on.
    print('EMERGENCY STOP')  # print on screen "EMERGENCY STOP"
    LeftHorizontal.value=0.00  #  Set pwm value for left horizontal esc to Zero
    RightHorizontal.value=0.00  # Set pwm value for right horizontal esc to Zero
    Left45.value=0.00  # Set pwm value for left vertical esc to Zero
    Right45.value=0.00  #  Set pwm value for right vertical esc to Zero
    
def button4():  #  Button 4 was assigned to open the claw
    print('Open Claw ')  #  print Open Claw on screen to confirm command received
    print (claw)  # print the claw value on screen to test how far open the claw is
    hand.value=claw  # Send the claw servo the value to open to

    
def button5():  #  Button 5 was assigned to close the claw
    print('Close Claw')  # print Close Claw on screen to confirm command received
    print (claw)  # print the claw value on screen to test how far closed the claw is
    hand.value=claw  #  Send the claw servo the value to close to

    
def button6():  # Button 6 was assigned to a servo to twist the arm clockwise
    print('Twist Right')  #  Print Twist Right on screen to confirm command received
    print (arm)  #  print the arm value on screen to test how far right the arm twists
    twist.value=arm  #  Send the arm servo the value to turn to
 
def button7():  #  Button 7 was assigned to a servo to twist the arm counter clockwise
    print('Twist Left')  # Print Twist Left on the screen to confirm command received
    print (arm)  # print the arm value on the screen to test how far left the arm twists
    twist.value=arm  #  Send the arm servo the value to turn to
    
def camoff():  #  Turn off the camera relay or set it to LOW to view the bottom camera
    print('Cam DOWN')  #  print Cam DOWN to confirm command received
    UpCam.off()  #  Set the camera LED pin to LOW to connect the down camera relay contacts
    
    
def camon():  # Turn on the camera relay or set it to HIGH to view the upper camera
    print ('Cam UP')  #  print Cam UP to confirm command received
    UpCam.on()  #  Set the camera LED pin to HIGH to connect the up camera relay contacts

    
def button8():  #  Assigned to set the claw and arm servos to a home position
    print('Button 8 SERVO HOME')  # print Button 8 SERVO HOME to confirm command received
    twist.value=0.0  #  Set the arm servo to its home position
    sleep(2)  #  sleep for 2 seconds to avoid overloading the 5 volt buss
    hand.value=0.0  #  Set the hand servo to its home position
    

def button10():  # Extra joystick button not used
    print('Button 10')
    
def button11():  # Extra joystick button not used
    print('Button 11')
    
def hat_up():  # Extra joystick button not used
    print('Hat Up')
    
def hat_down():  # Extra joystick button not used
    print('Hat Down')
    
def hat_left():  # Extra joystick button not used
    print('Hat Left')

def hat_right():  # Extra joystick button not used
    print('Hat Right')
    
def hat_centered():  # Extra joystick button not used
    print('Hat Centered')
    
while True:  #  MAIN LOOP   continuously run the following commands
    for event in pygame.event.get():  #  check if a joystick event occurred in pygame
        if event.type == pygame.JOYAXISMOTION:  #  If the pygame event = joystick axis event         
            direction = (event.axis)  # determine which axis was moved and assign it to direction
            power = (event.value)  #  read the value of the axis and assign it to power
            power = (power/4)  # divide the power by 4 and reassign it to power.  This is used to limit the esc's throughout the ROV.  A divide by 4 factor results in 25% maximum power to an esc.
            power = round(power,2)  # Round the power results to 2 decimal points for easier to read and work with numbers
            print (power, " ", direction)  # Display on the screen the power and axis direction number for testing and reference
            
            # LEFT MOTORS CODE
            

            if direction == 1 and power < -0.02: #   If the left stick is moved forward and the power is less than a - 0.02 for stick float run left_forward function
                left_forward()
            
            if direction == 1 and power  > 0.02:  #  If the left stick is moved backwards and the power is greater than 0.02 for stick float run left_reverse function
                left_reverse()
            
            if direction == 1 and abs((power) < 0.01) and abs((power) >-0.01):  # If the left stick is returned to center position then run the left_foward_reverse_stop function
                left_forward_reverse_stop()
            
            if direction == 0 and power < -0.02:  #   If the left stick is moved left and the power is less than a - 0.02 for stick float run left_up function
                left_up()
            
            if direction == 0 and power > 0.02:  #  If the left stick is moved right and the power is greater than 0.02 for stick float run left_down function
                left_down()
            
            if direction == 0 and abs((power) < 0.01) and abs((power) >-0.01):  # If the left stick has been returned to center run the left_up_down_stop function
                left_up_down_stop()
            
            
            #  RIGHT MOTORS CODE
            if direction == 3 and power < -0.02: #  If the right stick is moved forward and the power is less than a - 0.02 for stick float run right_forward function
                right_forward()
            
            if direction == 3 and power > 0.02:  #  If the right stick is moved backwards and the power is greater than 0.02 for stick float run right_reverse function
                right_reverse()
            
            if direction == 3 and abs((power) < 0.01) and abs((power) >-0.01):  # If the right stick is returned to center position then run the right_foward_reverse_stop function
                right_forward_reverse_stop()
                       
            if direction == 2 and power > 0.02:  #   If the right stick is moved right and the power is greater than 0.02 for stick float run right_up function
                right_up()
                
            if direction == 2 and power < -0.02:  #  If the right stick is moved left and the power is less than -0.02 for stick float run right_down function
                right_down()
            
            if direction == 2 and abs((power) < 0.01) and abs((power) >-0.01):  # If the right stick has been returned to center run the right_up_down_stop function
                right_up_down_stop()
                
        
        if event.type == pygame.JOYBUTTONDOWN:  #  If the event type is a joystick button press then run the following
            if event.button == 0:  #  if button 0 run blue function
                blue()
            if event.button == 1:  #  if button 1 run green function
                green()
            if event.button == 2:  # if button 2 run red_stop function
                red_stop()  #  This is where the EMERGENCY STOP event is detected.
            if event.button == 3:  # if button 3 run orange function
                orange()
            if event.button == 4:  # if button 4 open claw
                claw = claw - .2   # make claw servo steps -.2 per button press
                if claw < -.6:  # limit the servo steps to a maximum of -.6 to not over extend
                    claw = -.6
                button4()  # run button4 function
            if event.button == 5:  # if button 5 close claw
                claw = claw + .2  # make claw servo steps + .2 per button press
                if claw > 1:  # limit the servo steps to a maximum of 1 to not close past closed
                    claw = 1
                button5()  # run button5 function
            if event.button == 6: #  if button 6 twist arm clockwise
                arm = arm + .2  #  make arm servo steps + .2 per button press
                if arm > 1:  #  limit the servo steps to a maximum of 1 to not over rotate
                    arm = 1
                button6()  #  run button6 function
            if event.button == 7:  # if button 7 twist arm counterclockwise
                arm = arm - .2  # make arm servo steps - .2 per button press
                if arm < -1:  # limit the servo steps to a maximum of 1 to not over rotate
                    arm = -1
                button7()  #run button7 function
            if event.button == 8:  #  If button 8 run servo home code on button8 function
                button8()
            if event.button == 9:  # If button 9 is pressed and camera is off, turn on the top cam relay
                if cam == 0:
                    cam = 1
                    camon()
                else:
                    cam = 0  # If button 9 is pressed and camera is on, turn off the top cam relay
                    camoff()
            if event.button == 10:  #  if button 10 run extra button10 function
                button10()
            if event.button == 11:  # if button 11 run extra button11 function
                button11()
