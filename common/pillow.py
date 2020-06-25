#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

"""Wrapper module for Pillow - Python Imaging Library fork (https://github.com/python-pillow/Pillow)."""


class Pillow:
	def __init__(self, width, height):
		self.width = width
		self.height = height

	def create_image(self):
		# create blank image for drawing with 1-bit color
		image = Image.new('1', (self.width, self.height))
		draw = ImageDraw.Draw(image)

		# draw a white filled box to clear the image
		draw.rectangle((0, 0, self.width, self.height), outline=255, fill=255)

		return image, draw

	def draw_board(self, board):
		pillow = Pillow(self.width, self.height)
		image, draw = pillow.create_image()

		# draw board boundaries
		draw.rectangle((0, 0, self.width - 2, self.height - 2), outline=0, fill=255)

		# draw snake
		for i in range(len(board.snake.body)):
			x_1 = board.snake.body[i].x * 4
			y_1 = board.snake.body[i].y * 4

			if i == 0:
				# there is no previous point - draw head
				draw.rectangle((2 + y_1, 2 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)
				continue
			else:
				# else get previous point a form a rectangle with it
				x_0 = board.snake.body[i - 1].x * 4
				y_0 = board.snake.body[i - 1].y * 4

			if x_0 - x_1 == 0 and y_0 - y_1 == -4:
				# next body point is left
				draw.rectangle((1 + y_1, 2 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)
			elif x_0 - x_1 == -4 and y_0 - y_1 == 0:
				# next body point is up
				draw.rectangle((2 + y_1, 1 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)
			elif x_0 - x_1 == 0 and y_0 - y_1 == 4:
				# next body point is right
				draw.rectangle((2 + y_1, 2 + x_1, 5 + y_1, 4 + x_1), outline=0, fill=0)
			elif x_0 - x_1 == 4 and y_0 - y_1 == 0:
				# next body point is down
				draw.rectangle((2 + y_1, 2 + x_1, 4 + y_1, 5 + x_1), outline=0, fill=0)

		# draw food
		if board.food.x % 2 + 1 == 0:
			x = 3 + (board.food.x * 2)
			y = 3 + (board.food.y * 4)
		else:
			x = 3 + (board.food.x * 4)
			y = 3 + (board.food.y * 4)

		draw.point((y - 1, x))
		draw.point((y + 1, x))
		draw.point((y, x - 1))
		draw.point((y, x + 1))

		return image

	def draw_text(self, text):
		image, draw = self.create_image()
		font = ImageFont.load_default()
		draw.text((2, 2), text, font=font, fill=0)

		return image
