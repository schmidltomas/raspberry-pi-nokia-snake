#!/usr/bin/env python
import Adafruit_Nokia_LCD as LCD

"""Nokia LCD module using the Adafruit_Nokia_LCD library (https://github.com/adafruit/Adafruit_Nokia_LCD)."""


class NokiaLCD:
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
