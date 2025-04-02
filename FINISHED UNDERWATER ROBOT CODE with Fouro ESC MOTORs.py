import pygame #  This library allows us to read joystick positions and buttons
import time   #  This is to allow delays in our code
from gpiozero import LED  #  GPIOZERO is the library which allows us to remotely control our Raspberry Pi GPIO pins
from gpiozero import PWMLED #  GPIO function to turn on and off HIGH / LOW GPIO pins
from gpiozero import Button #  GPIO function to read a GPIO pin
from gpiozero import Servo  #  GPIO function to activate the thrusters.
                            #  ESC's are controlled like a servo using PWM.
#  Raising the PWM pulse width will increase the speed and lowering the pulse with will decrease the speed.
#  Sending a POSITIVE PWM VALUE will tell the motor to turn CLOCKWISE.
#  Sending a NEGATIVE PWM VALUE will tell the motor to turn COUNTER CLOCKWISE or ANTI CLOCKWISE.

from gpiozero.pins.pigpio import PiGPIOFactory  #  This library allows us to access the remote GPIO pins
                                                #  calling them locally using their Factory On Board pin numbers.

from time import sleep  #  This imports the sleep function from time.
#  I used this in troubleshooting, but not using it in the current code.

factory = PiGPIOFactory(host='192.168.0.130')  #  Using the PiGPIOFactory library connect all GPIO pins to a RPI
                                               #  on the network at IP address 192.168.0.126.  
red = LED(20, pin_factory=factory)  #  Test output pin to turn on and off an LED

# PINS: 6, 12, 16, 19.
# 6: 

LFA0 = LED(2, pin_factory=factory)       #  Left Front
LFA1 = LED(3, pin_factory=factory)
LFE1 = Servo(6, pin_factory=factory)    #  Regular motor controller pins used.

RFA2 = LED(5, pin_factory=factory)       #  Right Front
RFA3 = LED(7, pin_factory=factory)
RFE2 = Servo(12, pin_factory=factory)    #  Regular motor controller pins used.

LRB0 = LED(8, pin_factory=factory)       #  Left Rear
LRB1 = LED(9, pin_factory=factory)
LRE3 = Servo(16, pin_factory=factory)   #  Regular motor controller pins used.

RRB2 = LED(11, pin_factory=factory)      #  Right Rear
RRB3 = LED(13, pin_factory=factory)
RRE4 = Servo(19, pin_factory=factory)   #  Regular motor controller pins used.
# 
LHA0 = LED(23, pin_factory=factory)      #  Left Horizontal
LHA1 = LED(24, pin_factory=factory)
LHE1 = Servo(26, pin_factory=factory)   #  Regular motor controller pins used.

RHA2 = LED(22, pin_factory=factory)      #  Right Horizontal
RHA3 = LED(21, pin_factory=factory) 
RHE2 = Servo(25, pin_factory=factory)    #  This is the only pin that will be required to control a thruster.
                                         #  It is setup as a Servo PWM pin.

pygame.joystick.init()  #  Initialize the pygame joystick part of the program
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
#  Check how many joysticks are connected and assign them a number for reading access.
print(joysticks)  #  Print on the Shell the Joysticks connected
pygame.init()  # Initialize the pygame video system.
               #  Pygame is a game library which allows us to utilize the joysticks.
               #  Pygame can also be used to create video games.

direction = int  #  Assign an integer to direction.  This will be a positive or a negative number
                 #  we will use to determine which direction each stick has been moved.
                 #  NEGATIVE NUMBERS = UP and LEFT     and    POSITIVE NUMBERS = DOWN and RIGHT
power = float(0.00)  #  Assign a varible of power as a float.  This will be used to do calculations with PWM.
pwm = float(0.00)  #  Assign a variable of pwm as a float.
                   #  This will be the output value to control the motors speed
                   #  and for the SERVO(speed and direction)

#  All Subroutines need to be defined before they are called in Python.
#  The program will actually jump to the While Loop but keep these Subroutines in memory.
#  The programming in the While Loop will call these Subroutines based on Joytick Input Changes.
#  So in short all our Program is doing is keeping an eye on the joystick for any changes,
#  then based on those changes running this specific list of Subroutines.  FOREVER
def left_forward():  #Subroutines
    pwm = abs(power)  #  Calculate the absolute value of the power variable and assigning it to pwm.
                      #  This way our pwm value is forward.

   
    LFE1.value=pwm
    
def left_reverse():
    LFE1.value=-power

def left_forward_reverse_stop():
    LFE1.value=0
    
    

def left_up():
    pwm = abs(power)  


    LRE3.value=pwm
    

    
def left_down():
    pwm = abs(power)  
#     LFA0.off()
#     LFA1.on()
    LRE3.value=-pwm
#     
#  

def left_up_down_stop():
   
    LRE3.value=0
    
    
    LRE3.value=0
    
def right_forward():
    pwm = abs(power)  #  Calculate the absolute value of the power variable and assigning it to pwm.
                      #  This way our pwm value is forward.

   
    RFE2.value=pwm  #  This being a SERVO pin all we need to use to active a SERVO motor is send it a pwm signal.
    #  The pwm signal will give the motor DIRECTION and SPEED.
    #  SPEED is determined by a value of 0 to 1 and DIRECTION is determined by a + or - pwm value.
    #  The joystick Y axis moving foward / up produces a negative number, using the pwm = abs(power)
    #  we can turn it positive making the motor turn in the FORWARD DIRECTION
  
def right_reverse():
    pwm = abs(power)
    RFE2.value=-pwm#4.value=-power  #  The joystick Y Axis is providing a positive number
    #  so we add a negative before power to reverse the direction of the motor
    #  -power
    #  We could also rewire the motor the speed controller to reverse the direction,
    #  but this is a much easier way to manipulate the direction.

def right_forward_reverse_stop():
    RHE2.value=0  #  Setting the pwm value to 0  STOPS the thrust motor


def right_up():
    pwm = abs(power)  
#     RFA2.on()
#     RFA3.off()
    RRE4.value=pwm
    

    
def right_down():
    pwm = abs(power) 
#     RFA2.off()
#     RFA3.on()
    RRE4.value=-pwm
    
    
def right_up_down_stop():
#     RFA2.off()
#     RFA3.off()
    RFE2.value=0
    
    RRB2.off()
    RRB3.off()
    RRE4.value=0


def blue():
    print('Blue')
    
def green():
    print('Green')
    
def orange():
    print('Orange')
    
def red_stop():
    print('EMERGENCY STOP')  #  TURN OFF ALL PINS.  This comes in handy when making changes to the program
                             #  and a motor won't stop spinning because a mistake in the code.
    LFA0.off()
    LFA1.off()
    LFE1.value=0.00
    
    RFA2.off()
    RFA3.off()
    RFE2.value=0.00
    
    LRB0.off()
    LRB1.off()
    LRE3.value=0.00
    
    RRB2.off()
    RRB3.off()
    RRE4.value=0.00
    
    LHA0.off()
    LHA1.off()
    LHE1.value=0.00
    
    RHA2.off()
    RHA3.off()
    RHE2.value=0.00
    

def button4():
    print('Button 4')  #  These buttons can be used to activate addition motors or devices.

def button5():
    print('Button 5')  #  These buttons can be used to activate addition motors or devices.

def button6():
    print('Button 6')  #  These buttons can be used to activate addition motors or devices.
    
def button7():
    print('Button 7')  #  These buttons can be used to activate addition motors or devices.

def button8():
    print('Button 8')  #  These buttons can be used to activate addition motors or devices.
    
def button9():
    print('Button 9')  #  These buttons can be used to activate addition motors or devices.

def button10():
    print('Button 10')  #  These buttons can be used to activate addition motors or devices.
    
def button11():
    print('Button 11')  #  These buttons can be used to activate addition motors or devices.
    
def hat_up():  #  These Hat Subroutines could be used to level off the ROV if we were using 6 motors.
#     LFA0.off()
#     LFA1.off()
    LFE1.value=.2
#     
#     RFA2.off()
#     RFA3.off()
    RFE2.value=.2
    
#     LRB0.on()
#     LRB1.off()
    LRE3.value=.2
#     
#     RRB2.off()
#     RRB3.on()
    RRE4.value=.2
    
def hat_down():
    LFA0.on()
    LFA1.off()
    LFE1.value=.2
    
    RFA2.off()
    RFA3.on()
    RFE2.value=.2
    
    LRB0.off()
    LRB1.off()
    LRE3.value=.2
    
    RRB2.off()
    RRB3.off()
    RRE4.value=.2
def hat_left():
    LFA0.off()
    LFA1.off()
    LFE1.value=.2
    
    RFA2.on()
    RFA3.off()
    RFE2.value=.2
    
    LRB0.off()
    LRB1.off()
    LRE3.value=.2
    
    RRB2.off()
    RRB3.on()
    RRE4.value=.2
def hat_right():
    LFA0.on()
    LFA1.off()
    LFE1.value=.2
    
    RFA2.off()
    RFA3.off()
    RFE2.value=.2
    
    LRB0.off()
    LRB1.on()
    LRE3.value=.2
    
    RRB2.off()
    RRB3.off()
    RRE4.value=.2
    
def hat_centered():  #  When the Hat Switch is returned to center /  a Hat Switch release,
                     #  this Subroutine will turn off all motors.
    LFA0.off()
    LFA1.off()
    LFE1.value=0.00
    
    RFA2.off()
    RFA3.off()
    RFE2.value=0.00
    
    LRB0.off()
    LRB1.off()
    LRE3.value=0.00
    
    RRB2.off()
    RRB3.off()
    RRE4.value=0.00
    
    LHA0.off()
    LHA1.off()
    LHE1.value=0.00
    
    RHA2.off()
    RHA3.off()
    RHE2.value=0.00
    
while True:  #  This is the main part of the program that loops continuously until the program is stopped.
             #  It receives joystick events and calls Subroutines for each event.
    for event in pygame.event.get():  #  Using the pygame library, get a joystick event.
                                      #  Any change in a button press or stick movement causes an event.

        if event.type == pygame.JOYAXISMOTION:  #  If an event is a joystick moving, run the following code.
            
            direction = (event.axis) #  Assign the specific joystick axis direction to the direction variable
            power = (event.value)    #  Assign how much the joystick was moved in the direction
                                     #  to the power variable.
            power = round(power, 2)  #  Round the power numbers to the Hundredths place,
                                     #  so we can work with less digits.
            power = (power/4)  #  Limit all motor speeds to 1/2 possible power by dividing by 2.
            print (power)  #  Print the power level on the Shell
            
            
            # LEFT MOTORS CODE
            if direction == 1 and power < -0.02:  #  If the left stick is being pressed Up on it's Y axis.
                                                  #  Check that the power is above the center for joystick error.
                left_forward()  # Run the left_forward Subroutine
            if direction == 1 and power  > 0.02:  #  If the left stick is being pressed Down on it's Y axis.
                                                  #  Check that the power is above the center for joystick error.
                left_reverse()  # Run the left_reverse Subroutine
            if direction == 1 and abs((power) < 0.01) and abs((power) >-0.01): #  If the stick is not being pressed
                                                                               #  Stop the Motor
                left_forward_reverse_stop()  #  Run the motor left_forward_reverse_stop Subroutine
            
            if direction == 0 and power < -0.02:  #  This is similar code for the X Axis of the left stick.
                                                  #  This would allow two motors to move the ROV up and down.
                left_up()
            if direction == 0 and power > 0.02:
                left_down()
            if direction == 0 and abs((power) < 0.01) and abs((power) >-0.01):
                left_up_down_stop()
            
            
            #  RIGHT MOTORS CODE
            if direction == 3 and power < -0.02:  #  Same as the left stick, just calling Subroutines for the
                                                  #  Right Stick Motors
                right_forward()
            if direction == 3 and power > 0.02:
                right_reverse()
            if direction == 3 and abs((power) < 0.01) and abs((power) >-0.01):
                right_forward_reverse_stop()
            
            if direction == 2 and power < -0.02:
                right_down()
            if direction == 2 and power > 0.02:
                right_up()
            if direction == 2 and abs((power) < 0.01) and abs((power) >-0.01):
                right_up_down_stop()
                
        
        #  HAT LEVELING MOTORS CODE
        if event.type == pygame.JOYHATMOTION:  #  If an event is a hat switch being pressed run the following code.
            if event.value == (0, 0):
                hat_centered()
            if event.value == (1, 0):
                hat_right()
            if event.value == (-1, 0):
                hat_left()
            if event.value == (0, 1):
                hat_up()
            if event.value == (0, -1):
                hat_down()
        
        #  EXTRA BUTTONS CODE
        if event.type == pygame.JOYBUTTONDOWN:  # if an event is a button being pressed run the following code.
            if event.button == 0:
                blue()
            if event.button == 1:
                green()
            if event.button == 2:
                red_stop()  #  This is where the EMERGENCY STOP event is detected.
            if event.button == 3:
                orange()
            if event.button == 4:
                button4()
            if event.button == 5:
                button5()
            if event.button == 6:
                button6()
            if event.button == 7:
                button7()
            if event.button == 8:
                button8()
            if event.button == 9:
                button9()
            if event.button == 10:
                button10()
            if event.button == 11:
                button11()