#!/usr/bin/env python
from PIL import Image, ImageDraw, ImageFont

"""Wrapper module for Pillow - Python Imaging Library fork (https://github.com/python-pillow/Pillow)."""


class Pillow:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def get_image(self):
		# create blank image for drawing with 1-bit color
		image = Image.new('1', (self.width, self.height))
		draw = ImageDraw.Draw(image)

		# draw a white filled box to clear the image
		draw.rectangle((0, 0, self.width, self.height), outline=255, fill=255)

		return image, draw

	def get_text(self, text):
		image, draw = self.get_image()
		font = ImageFont.load_default()
		draw.text((2, 2), text, font=font, fill=0)

		return image
