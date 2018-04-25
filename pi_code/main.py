#from termcolor import colored
import time
import os
import picamera
#from Adafruit-Raspberry-Pi-Python-Code/Adafruit_BMP085 import BMP085
from Adafruit_BMP085 import BMP085
import Adafruit_DHT
import RPi.GPIO as GPIO
import thread

runtime = 0
end_time  = 3*60*60

for_sure_landed = False

hans = 0
time_name = ''
filename_time = 'noName'
intervall = 5


innerTemperature_package = ''
outerTemperature_package = ''
pressure_package = ''
humidity_package = ''
height_package = ''
#pos_package = ''


#for to check weather to blink or not
blinking  = False
current_height  = 0
old_height = 0
height_difference = 0
on_zone  = 2000

camera = picamera.PiCamera()
bmp = BMP085(0x77)
humidity_sensor = Adafruit_DHT.DHT22 # geaendert von 11->22
humidity_pin = 26 #der pin an dem der luftfeuchtigkeit-sensor angeschlossen ist

led_pin = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)


def get_time_gmt():
	
	return time.localtime(time.time()) #very likly getting time that way wont work in rasspberry pi. use that time hardware fuck

# led stuff

def led_on(pin):
	GPIO.output(pin, GPIO.HIGH)
def led_off(pin):
	GPIO.output(pin, GPIO.LOW)

def blink():

	
	
	global on_zone
	global height_difference
	global for_sure_landed
	global led_pin
	global current_height

	been_in_sky = False
	flying  = False
	blinking = True
	pin = led_pin

	timer_running = False
	waiting_time_over = False
	landing_time  = 0
	critical_time = 2 * 60
	waiting_time = (2 * 60 * 60) + (20 * 60) 

	start_time = 0


	while 1:
		lBlinking = blinking
		global current_height
		global height_difference
		#check if flying 
		print "blinkloop"
		if height_difference > 2:
			flying = True
			#print "     !!!!FLYING SET TRUE!!!!!!! <3"
		else:
	 		flying = False

	 	if been_in_sky == False and current_height > 3000:
	 		been_in_sky = True

	 	#control timer
	 	if flying == True and for_sure_landed == False and timer_running == True:
			timer_running = False
		elif timer_running == True and waiting_time_over == False:
	 		if time.time() - start_time > critical_time and for_sure_landed == False:
	 			for_sure_landed = True
			elif time.time() - start_time >= waiting_time:
				waiting_time_over = True 
		elif flying == False and timer_running == False and been_in_sky == True:
	 		timer_running = True
	 		start_time = time.time()
	 

	 	#leds on or off
	 	if flying == False and been_in_sky == False:
	 		blinking = True
	 	elif flying == False and been_in_sky == True and waiting_time_over == True:
	 		blinking = True
		elif flying == True:
	 		blinking = False 
		

		if blinking == False and for_sure_landed == True and waiting_time_over == False:
			#print "                 START DEEP SLEEP"
			time.sleep(waiting_time)
			#print "			END DEEP SLEEP"
	 	elif blinking == False and lBlinking == False:
	 		time.sleep(5)
		elif blinking == True and been_in_sky == False:
			led_on(pin)
			time.sleep(.1)
			led_off(pin)
			time.sleep(.3)
			led_on(pin)
			time.sleep(.1)
			led_off(pin)
			time.sleep(.3)
		elif blinking == True and been_in_sky == True:
			led_on(pin)
			time.sleep(.1)
			led_off(pin)
			time.sleep(5)
		elif blinking == False and lBlinking == True:
			led_off(pin)


		'''print "in blink"             
		print "  height_difference: "       ,  height_difference
		print "  current height: "   , current_height
		print "  been_in_sky:  "     , been_in_sky
		print "  flying: "           , flying
		print "  blinking: "         , blinking
		print "  timer_running: "    , timer_running
		print "  for_sure_landed: "  , for_sure_landed
		print "  waiting_time_over: ", waiting_time_over
		print "\n"
		'''
		print "runtime: ", runtime				

#meassuring stuff

def picture_loop():
	
	global for_sure_landed
	global runtime
	global end_time
	global filename_time
	while for_sure_landed == False or runtime < end_time:
		starttime  = time.time()
		print "pictureloop"
		#string = 'streamer -f jpeg -o ./pictures/' + filename_time + '.jpeg' #use a different command, this command doesn't work for rasspberry pi cam
		#os.system(string)
		#print colored("Cheese!", "green")
		string = camera.capture('./pictures/' + filename_time + '.jpg') 
		#print colored(("picture_saved: ", filename_time, ".jpg"), "green")
		stime = 5 - (time.time() - starttime)
		if stime >0:
			time.sleep(stime)
		else:
			print "WARNING: picture loop to long: ", stime
	print "pictureloop end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"

def takeAndPackage_outerTemperature():
	#print colored("starting temperature measurement", "cyan")
	global outerTemperature_package

	output = os.popen('cat /sys/bus/w1/devices/28-04169394d2ff/w1_slave').read()# PFAD UND ID ANPASSEN
	#temperature = os.popen('echo "scale=2; "\'echo${tempread##*=}\'" / 1000" | bc').read()
	temperature = ""
	oldChar = None
	adding = False
	for char in output:

		if adding == True and char != '\n':
			temperature += char			
			

		if char == '=' and oldChar == 't':
			adding = True		

		oldChar = char	
	temperature = float(temperature)/1000

	outerTemperature_package += 'TEMPERATURE   |   DATE: ' + filename_time + '   |   VALUE: ' + str(temperature) + "\n"
	#print "outerTemperature measured: ", str(temperature) 

def takeAndPackage_innerTemperature():

	global innerTemperature_package

	temperature = bmp.readTemperature()

	innerTemperature_package += "TEMPERATURE   |   DATE: " + filename_time + "   |   VALUE:" + str(temperature) + "\n"	
	#print "innerTemperature measured: ", str(temperature)
	#print colored("temperature measurement finished", "cyan")

def takeAndPackage_pressure():

	#print colored("starting pressure measurement", "magenta")
	global pressure_package

	#pressure = 33 #replace 33 with command(s) to get pressure data 
	pressure = bmp.readPressure()
	#pressure = os.system("python /home/pi/Adafruit-Raspberry-Pi-Python-Code/Adafruit_BMP085/Adafruit_BMP085_example.py")
	pressure = float(pressure) / 100
	pressure_package += 'PRESSURE   |   DATE: ' + filename_time + '   |   VALUE: ' + str(pressure) + "\n" 
	#print "pressure measured: ", str(pressure)
	#print colored("pressure measurement finished", "magenta")


def takeAndPackage_humidity():

	#print colored("starting humidity measurement", "blue")
	global humidity_package

	#humidity = 33 #replace 33 with command(s) to get temperature data 
	humidity, temperature = Adafruit_DHT.read_retry(humidity_sensor, humidity_pin)

	humidity_package += 'HUMIDITY   |   DATE: ' + filename_time + '   |   VALUE: ' + str(humidity) + "\n" 
	#print "humidity measured: ", str(humidity)
	#print colored("humidity measurement finished", "blue")	


def takeAndPackage_height():

	#print colored("starting height measurement", "yellow")
	global height_package
	global current_height


	current_height = bmp.readAltitude()

	height_package += 'HEIGHT   |   DATE: ' + filename_time + '   |    VALUE: ' + str(current_height) + "\n"

	#print "height measured: ", str(current_height)
	#print colored("height measurement finished", "yellow")

'''
def takeAndPackage_Position():

	#print "					start Package Position"

	pos = os.system(cgps -s)

	pos_package += pos

	#print "					end package position"
'''

def save_packages():
	
	#print colored("saving packages...", "white", "on_blue")

	global innerTemperature_package

	with open("innerTemperature.pro", "a") as innerTemperatureFile:
		innerTemperatureFile.write(innerTemperature_package)

	innerTemperature_package = ''
	#print "    innerTemperature saved"


	global outerTemperature_package

	with open("outerTemperature.pro", "a") as outerTemperatureFile:
		outerTemperatureFile.write(outerTemperature_package)

	outerTemperature_package = ''
	#print "    outerTemperature saved"	

	
	global pressure_package

	with open("pressure.pro", "a") as pressureFile:
	    pressureFile.write(pressure_package)
	#print "    pressure saved"


	global humidity_package

	with open("humidity.pro", "a") as humidityFile:
	    humidityFile.write(humidity_package)

	humidity_package = ''
	#print "    humidity saved"
	

	global height_package

	with open("height.pro", "a") as heightFile:
		heightFile.write(height_package)

	height_package = ''
	#print "    height saved"	


	#print colored("all packages saved", "white", "on_blue")


	'''global pos_package

	with open ("position.pro", "a") as posFile:
		posFile.write(pos_package)

	pos_package = ''
	#print "						pos saved"
	'''


def main():

	thread.start_new_thread(blink, () )
	thread.start_new_thread(picture_loop, () )

	packageSize = intervall - 1
	dt = 0
	secondloop = False
	loopTime = 5



	#start gps stuff 
	#WARNING: this will only init gps stuff at start, maybe you have to pu this inside takeAndPackage_position
	#start the serial port:
	#os.system(stty -F /dev/ttyAMA0 9600)
	#start GPSD:
	#os.system(sudo gpsd /dev/ttyAMA0 -F /var/run/gpsd.sock)

	#while for_sure_landed == False: only use this when ure 100 precent sure it works
	while 1:

		print "mainloop"
		global runtime
		global current_height
		global old_height
		global height_difference
		global end_time
		
		start_time = time.time() #time.time() may not work
		
		if runtime < end_time or for_sure_landed == False:
			print "measureloop"
			time_name = str(time.asctime( time.localtime(time.time()) )) #very likly getting time that way wont work in rasspberry pi. use that time hardware fuck
		
			global filename_time
			
			filename_time = ''
			for char in time_name:
				if char == " ":
					char = '_'
				elif char == ":":
					char = '-'
	
				filename_time += char



			 
			
			takeAndPackage_outerTemperature()
			takeAndPackage_innerTemperature()
			#time.sleep(1)
			takeAndPackage_pressure()
			#time.sleep(1)
			takeAndPackage_humidity()
			#time.sleep(1)
			takeAndPackage_height()

			packageSize += 1

		
			if packageSize == intervall:
				save_packages()
				packageSize = 0

	
		lend_time = time.time() #time.time() may not work
		dt = lend_time - start_time
		if dt>loopTime:
			#print colored(str("warning: dt > " + str(loopTime)), "red")
			#print "dt: ", dt
			pass

		else:
			#print "waiting: ", (loopTime -dt), " seconds ..."	
			time.sleep((loopTime - dt))
		#print "\nloop End \n"


		#DONT komment this out
		height_difference = abs(old_height - current_height)
		old_height = current_height
		

		runtime += time.time() - start_time



main()

