import time

import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI

from PIL import Image, ImageDraw


class NokiaLCD():
	# SPI config (defaults to bit-bang SPI interface):
	display = LCD.PCD8544(dc=27, rst=23, sclk=17, din=18, cs=22)
	width = LCD.LCDWIDTH
	height = LCD.LCDHEIGHT
	
	def __init__(self):
		self.display.begin(contrast=60)
		self.display.clear()
		self.display.display()
		
	def display_image(self, image):
		self.display.image(image)
		self.display.display()
