import RPi.GPIO as GPIO # import our GPIO module
import time
from subprocess import call

# add the following line to /boot/config.txt
# dtoverlay=gpio-poweroff,gpiopin=25,active_low
# dtoverlay=gpio-poweroff,gpiopin=7,active_low

# Then create the service
# make file executable
# chmod +x /home/pi/carPiHat.py

#Create a service
# sudo nano /etc/systemd/system/carpihat.service

#Add the default lines required below

# [Unit]
# Description=CarPiHat initialisation

# [Service]
# Type=simple

# ExecStart=/usr/bin/python3 /home/pi/carPiHat.py

# [Install]
# WantedBy=multi-user.target

GPIO.setmode(GPIO.BCM) # we are using BCM pin numbering

IGN_PIN = 12		# our 12V switched pin is BCM12
EN_POWER_PIN = 25	# our latch pin is BCM25

EN_AMP_PIN = 7 #amplifier enable pin

IGN_LOW_TIME = 5 # time (s) before a shutdown is initiated after power loss

GPIO.setup(IGN_PIN, GPIO.IN) # set our 12V switched pin as an input

GPIO.setup(EN_POWER_PIN, GPIO.OUT, initial=GPIO.HIGH) # set our latch as an output
GPIO.setup(EN_AMP_PIN, GPIO.OUT, initial=GPIO.HIGH)

GPIO.output(EN_POWER_PIN, 1) # latch our power. We are now in charge of switching power off
GPIO.output(EN_AMP_PIN, 1)

ignLowCounter = 0

while 1:
	if GPIO.input(IGN_PIN) != 1: 				# if our 12V switched is not disabled
		time.sleep(1)							# wait a second
		ignLowCounter += 1						# increment our counter
		if ignLowCounter > IGN_LOW_TIME:		# if it has been switched off for >5s
			GPIO.output(EN_AMP_PIN, 0)
			print("Shutting Down")
			call("sudo shutdown -h now", shell=True)	# tell the Pi to shut down
	else:
		ignLowCounter = 0 						# reset our counter, 12V switched is HIGH again
		GPIO.output(EN_AMP_PIN, 1)
		time.sleep(0.5)  # Add a small sleep delay to reduce CPU usage