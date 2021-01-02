# Import required libraries
import time
import board
from digitalio import DigitalInOut, Direction, Pull
import adafruit_dotstar
import analogio

class FeatherS2:
	def __init__(self):
		# the boot button !
		self._boot = DigitalInOut(board.IO0)
		self._boot.switch_to_input(pull=Pull.UP)
		
		# pin 13 and on-board RGB
		self._led13 = DigitalInOut(board.LED)
		self._led13.direction = Direction.OUTPUT
		self._dotstar = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.5, auto_write=True)
		
		# the second LDO
		self._ldo2 = DigitalInOut(board.LDO2)
		self._ldo2.direction = Direction.OUTPUT
		
		# ambient light sensor
		self._light = analogio.AnalogIn(board.AMB)
	
	"""Reading the on-board multipurpose button known as boot"""
	@property
	def boot(self):
		return not self._boot.value

	"""The pin 13 is blue"""
	@property
	def blue_led(self):
		return self._led13.value
	@blue_led.setter
	def blue_led(self,value):
		#set the internal LED IO13 to it's inverse state
		self._led13.value = value

	"""Set the power for the second on-board LDO to allow no current draw when not needed."""
	@property
	def ldo2(self):
		return self._ldo2.value
	@ldo2.setter
	def ldo2(self,state):
		# Set the LDO2 power pin on / off
		self._ldo2.value = state
		# A small delay to let the IO change state
		time.sleep(0.035)
	
	"""Old style convenience function for enabling LDO2"""
	def enable_LDO2(self,state):
		self.ldo2 = state

	"""On board RGB LED, otherwise used for Circuitpython status"""
	@property
	def dot(self):
		return self._dotstar
	
	"""Color wheel to allow for cycling through the rainbow of RGB colors."""
	@staticmethod
	def wheel(wheel_pos):
		wheel_pos = wheel_pos % 255
		if wheel_pos < 85:
			return 255 - wheel_pos * 3, 0, wheel_pos * 3
		elif wheel_pos < 170:
			wheel_pos -= 85
			return 0, wheel_pos * 3, 255 - wheel_pos * 3
		else:
			wheel_pos -= 170
			return wheel_pos * 3, 255 - wheel_pos * 3, 0

	"""Light, the friendly light sensor (516-52686) - make a percent version ? (0-100)"""
	@property
	def light(self):
		return self._light.value

fs2 = FeatherS2()
# Enable LDO2 by default
fs2.enable_LDO2(True)
