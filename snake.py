#!/usr/bin/env python
from enum import Enum
from image_pil import Img

import random


class Point:
	"""Base class for all points on the board with x and y coordinates."""
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self, x, y):
		print('.', end='')


class Food(Point):
	"""Food for the snake."""
	def __init__(self, x, y):
		Point.__init__(self, x, y)

	def draw(self, x, y):
		print('X', end='')


class Direction(Enum):
	"""Direction in which the snake moves."""
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4

	@staticmethod
	def from_key(input_key):
		if input_key == 'w':
			return Direction.UP
		elif input_key == 's':
			return Direction.DOWN
		elif input_key == 'a':
			return Direction.LEFT
		elif input_key == 'd':
			return Direction.RIGHT


class Snake(Point):
	"""The snake - represented by a list of Points."""
	body = [Point]
	direction = Direction.RIGHT

	def __init__(self, x, y):
		Point.__init__(self, x, y)
		self.body = [Point(x, y - i) for i in range(9)]

	def head(self):
		return self.body[0]

	def tail(self):
		return self.body[len(self.body) - 1]

	def eat(self):
		self.body.append(Point(self.tail().x, self.tail().y))

	def move_body(self):
		i = len(self.body) - 1
		while len(self.body) > i > 0:
			self.body[i].x = self.body[i - 1].x
			self.body[i].y = self.body[i - 1].y
			i -= 1

	def validate_direction(self, new_direction):
		if new_direction == Direction.UP and self.direction == Direction.DOWN \
				or new_direction == Direction.DOWN and self.direction == Direction.UP \
				or new_direction == Direction.LEFT and self.direction == Direction.RIGHT \
				or new_direction == Direction.RIGHT and self.direction == Direction.LEFT:
			return False
		else:
			return True

	def draw(self, x, y):
		if x == self.body[0].x and y == self.body[0].y:
			print('O', end='')
		else:
			print('o', end='')


class CollisionException(Exception):
	pass


class Board:
	"""Playing board."""
	snake = Snake
	food = Food
	score = 0

	def __init__(self, width, height, snake, food, lcd):
		self.width = width
		self.height = height
		self.board = [[Point(0, 0) for x in range(self.height)] for y in range(self.width)]
		self.snake = snake
		self.food = food
		self.lcd = lcd

		# init snake position
		for body_point in self.snake.body:
			self.board[body_point.x][body_point.y] = self.snake

		# init food position
		self.board[self.food.x][self.food.y] = self.food

	def to_image(self):
		img = Img(self.lcd.width, self.lcd.height)
		image, draw = img.get_image()

		# draw board boundaries
		draw.rectangle((0, 0, self.lcd.width-2, self.lcd.height-2), outline=0, fill=255)

		# draw snake
		for i in range(len(self.snake.body)):
			x_1 = self.snake.body[i].x * 4
			y_1 = self.snake.body[i].y * 4
			x_0 = self.snake.body[i - 1].x * 4
			y_0 = self.snake.body[i - 1].y * 4

			if x_0 - x_1 == 0 and y_0 - y_1 == -4:
				draw.rectangle((0 + y_1, 2 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)
				# snake body turns left
			elif x_0 - x_1 == -4 and y_0 - y_1 == 0:
				draw.rectangle((2 + y_1, 1 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)
				# snake body turns up
			elif x_0 - x_1 == 0 and y_0 - y_1 == 4:
				draw.rectangle((2 + y_1, 2 + x_1, 5 + y_1, 4 + x_1), outline=0, fill=0)
				# snake body turns right
			elif x_0 - x_1 == 4 and y_0 - y_1 == 0:
				draw.rectangle((2 + y_1, 2 + x_1, 4 + y_1, 5 + x_1), outline=0, fill=0)
				# snake body turns down
			else:
				# no previous point - head
				draw.rectangle((2 + y_1, 2 + x_1, 4 + y_1, 4 + x_1), outline=0, fill=0)

		# draw food
		if self.food.x % 2 + 1 == 0:
			x = 3 + (self.food.x*2)
			y = 3 + (self.food.y*4)
		else:
			x = 3 + (self.food.x*4)
			y = 3 + (self.food.y*4)

		draw.point((y - 1, x))
		draw.point((y + 1, x))
		draw.point((y, x - 1))
		draw.point((y, x + 1))

		return image

	def to_stdout(self):
		for x in range(self.width):
			for y in range(self.height):
				self.board[x][y].draw(x, y)
			print()

		print('Score: {0}'.format(self.score))

	def next_turn(self, new_direction):
		# check if snake's new direction is valid
		if self.snake.validate_direction(new_direction):
			self.snake.direction = new_direction

		next_point = Point
		head = self.snake.head()
		if self.snake.direction == Direction.UP:
			next_point = Point(head.x - 1, head.y)
		elif self.snake.direction == Direction.DOWN:
			next_point = Point(head.x + 1, head.y)
		elif self.snake.direction == Direction.LEFT:
			next_point = Point(head.x, head.y - 1)
		elif self.snake.direction == Direction.RIGHT:
			next_point = Point(head.x, head.y + 1)

		self.detect_collision(next_point)
		self.spawn_new_food(next_point)

		# move the snake's body (without head)
		self.snake.move_body()
		# update snake head position on the board
		self.board[next_point.x][next_point.y] = self.snake
		head.x = next_point.x
		head.y = next_point.y

	def detect_collision(self, next_point):
		if next_point.x == self.width or next_point.y == self.height or next_point.x == -1 or next_point.y == -1:
			raise CollisionException
		elif isinstance(self.board[next_point.x][next_point.y], Snake):
			raise CollisionException

	def spawn_new_food(self, next_point):
		# if the next point is Food, eat it and spawn a new one
		if isinstance(self.board[next_point.x][next_point.y], Food):
			x = random.randint(0, self.width - 1)
			y = random.randint(0, self.height - 1)

			# spawn new food on the board, not on the snake or the current food
			while isinstance(self.board[x][y], Snake) or \
					x == self.board[next_point.x][next_point.y].x and y == self.board[next_point.x][next_point.y].y:
				x = random.randint(0, self.width - 1)
				y = random.randint(0, self.height - 1)

			self.food.x = x
			self.food.y = y
			self.board[x][y] = Food(x, y)
			self.snake.eat()
			self.score += 1
		else:
			# else set last tail point from Snake to Point type
			tail = self.snake.tail()
			self.board[tail.x][tail.y] = Point(0, 0)
