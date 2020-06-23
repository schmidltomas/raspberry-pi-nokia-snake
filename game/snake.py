#!/usr/bin/env python
from enum import Enum

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

	def __init__(self, width, height, snake, food):
		self.width = width
		self.height = height
		self.board = [[Point(0, 0) for x in range(self.height)] for y in range(self.width)]
		self.snake = snake
		self.food = food

		# init snake position
		for body_point in self.snake.body:
			self.board[body_point.x][body_point.y] = self.snake

		# init food position
		self.board[self.food.x][self.food.y] = self.food

	def next_turn(self, new_direction):
		# check if snake's new direction is valid
		if self.snake.validate_direction(new_direction):
			self.snake.direction = new_direction

		# determine position of next point
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

	def to_stdout(self):
		for x in range(self.width):
			for y in range(self.height):
				self.board[x][y].draw(x, y)
			print()

		print('Score: {0}'.format(self.score))
