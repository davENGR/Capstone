"""This code is for the Maverick Auction Box Capstone Project
This file is for the RaspberryPi that handles the current scale data being read in
from the Indicator and through the MAX332 chip that shifts the voltage swing to nominal 5 V TTL or to 3.3 V
After reading in the data, it will then display the read in data either in the desired 'Oklahoma' or 'Texas' mode.
And when new values are read in, the previous values are then feed to the next RaspberryPi using UART"""

"""Written by David Wesson and Cooper Duncan"""

import serial, time, pygame, sys
import RPi.GPIO as GPIO
from pygame.locals import *
pygame.init()

TIMEOUT = 1.0 # 1 second timeout for reading UART
BAUD_RATE = 9600

mode_pin = 17 # Pin 11 on Pi. Used for Texas/Oklahoma selection
ready_pin = 2 # Pin 3 on Pi. Used to tell when 2nd Pi is ready
debug_led = 18 # Pin 12 on Pi. Used for debugging

SCREEN_WIDTH = 800 #common values seen passed for these variables
SCREEN_HEIGHT = 600

#to set the screen to fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN, 32)
screen.fill((255,255,255))#sets the background to RED

# Returns a string value to send to the 2nd Pi
# "t\nweightvalue\nheadvalue\navgvalue where t is for Texas output (replace with o for Oklahoma)
def transfer_string(b,w,h,a):
	s = ""
	if b == True:
		s = "o"
	else:
		s = "t\n"
	s = s + str(w) + "\n"
	s = s + str(h) + "\n"
	s = s + str(a) + "\n"
	#print s # Used for debugging
	return s
	
#Check Oklahoma/Texas mode switch, return True if Oklahoma mode	
def check_mode():
	if GPIO.input(mode_pin):
		return True
	else:
		return False
	return

def text_objects(curr_weight, curr_head, curr_ave): #subroutine to continually be called to refresh the displayed contents
	textFont = pygame.font.Font(None, 72)
	
	#setup for line of text to display the weight
	text_weight_surf = textFont.render('WT: %d' %curr_weight, True, (0,0,0))
	text_weight_rect = text_weight_surf.get_rect()
	
	#setup for line of text to display the head
	text_head_surf = textFont.render('HD: %i' %curr_head, True, (0,0,0))
	text_head_rect = text_head_surf.get_rect()
	
	#setup for line of text to display the average weight
	text_ave_surf = textFont.render('WT: %d' %curr_ave, True, (0,0,0))
	text_ave_rect = text_ave_surf.get_rect()
	
	return text_weight_surf, text_weight_rect, text_head_surf, text_head_rect, text_ave_surf, text_ave_rect
	
def update_display(disp_version, curr_weight, curr_head, curr_ave): #subroutine to continually be called to refresh the displayed contents
	weight_surf, weight_rect, head_surf, head_rect, ave_surf, ave_rect = text_objects(curr_weight, curr_head, curr_ave)
	
	#if bit version equals Texas
	if disp_version:
		weight_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2 - head_rect.get_height()))
		screen.blit(weight_surf, weight_rect)
		
		#update the display as needed
		pygame.display.update()
		
	else:
		#define and tweek the spacing of where the lines will be drawn on the screen
		weight_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2 - head_rect.get_height()))
		head_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
		ave_rect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2 + head_rect.get_height()))
	
		#render the lines onto the screen
		screen.blit(weight_surf, weight_rect)
		screen.blit(head_surf, head_rect)
		screen.blit(ave_surf, ave_rect)
	
		#update the display as needed
		pygame.display.update()
	return

def main():
	weight_current = 0.0
	weight_prev = 0.0
	head_current = 0
	head_prev = 0
	avg_current = 0.0
	avg_prev = 0.0
		
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(mode_pin, GPIO.IN)
	GPIO.setup(ready_pin, GPIO.IN)
	GPIO.setup(debug_led, GPIO.OUT)
	
	# This will be used to detect when 2nd pi is ready
	#while GPIO.input(ready_pin) == 0:
	#	time.sleep(1)
	
	# Start the serial connection	
	uart = serial.Serial("/dev/ttyAMA0", baudrate=BAUD_RATE, timeout=TIMEOUT)
	uart.open()
	
	GPIO.output(debug_led, True) # Signal that the program has started
	
	b_Oklahoma = check_mode() # True if mode is Oklahoma, false if Texas
	
	# First update of display and write zero values to 2nd Pi
	update_display(b_Oklahoma, weight_current, head_current, avg_current)
	uart.write(transfer_string(b_Oklahoma, weight_prev, head_p
	
		
	while True:
		#verify that the user is not exitting the system
		if pygame.event == QUIT
			pygame.quit()
			sys.exit()
		#otherwise continue
		
		mode = check_mode()
		#If the mode has changed update both displays
		if b_Oklahoma != mode :
			b_Oklahoma = mode
			update_display(b_Oklahoma, weight_current, head_current, avg_current)
			uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
			
		input = uart.readline()
		
		if input != '':
			if 'a' in input:
				input = uart.readline()
				input = input[0:len(input)-2]
				weight_prev = weight_current
				weight_current = float(input)
				update_display(b_Oklahoma, weight_current, head_current, avg_current)
				uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
			
			elif 'b' in input:
				input = uart.readline()
				input = input[0:len(input)-2]
				head_prev = head_current
				head_current = int(input)
				input = uart.readline()
				avg_prev = avg_current
				avg_current = float(input)
				update_display(b_Oklahoma, weight_current, head_current, avg_current)
				uart.write(transfer_string(b_Oklahoma, weight_prev, head_prev, avg_prev))
				
	return
		
main()
