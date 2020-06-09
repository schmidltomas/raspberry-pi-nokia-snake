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

	def key(self):
		if self == 'w':
			return Direction.UP
		elif self == 's':
			return Direction.DOWN
		elif self == 'a':
			return Direction.LEFT
		elif self == 'd':
			return Direction.RIGHT

		
class Snake(Point):
	"""The snake itself - represented by a list of body Points."""
	body = [Point]
	direction = Direction.RIGHT
	
	def __init__(self, x, y):
		Point.__init__(self, x, y)
		self.body = [Point(x, y), Point(x, y - 1), Point(x, y - 2), Point(x, y - 3)]
		
	def head(self):
		return self.body[0]

	def tail(self):
		return self.body[len(self.body) - 1]
		
	def eat(self):
		self.body.append(Point(self.tail().x, self.tail().y))

	def move_body(self):
		k = len(self.body) - 1 
		while len(self.body) > k > 0:
			self.body[k].x = self.body[k - 1].x
			self.body[k].y = self.body[k - 1].y
			k -= 1

	def check_direction(self, direction):
		if direction == Direction.UP and self.direction == Direction.DOWN \
				or direction == Direction.DOWN and self.direction == Direction.UP \
				or direction == Direction.LEFT and self.direction == Direction.RIGHT \
				or direction == Direction.RIGHT and self.direction == Direction.LEFT:
			raise DirectionException

	def draw(self, x, y):
		if x == self.body[0].x and y == self.body[0].y:
			print('O', end='')
		else:
			print('o', end='')


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
	
	def draw(self):
		# draw snake on board
		for body_point in self.snake.body:
			self.board[body_point.x][body_point.y] = self.snake

		# draw food
		self.board[self.food.x][self.food.y] = self.food

		# draw board
		for x in range(self.width):
			for y in range(self.height):
				self.board[x][y].draw(x, y)
			print()

	def print_score(self):
		print('Score: {0}'.format(self.score))

	def spawn_new_food(self, next_point):
		if isinstance(next_point, Food):
			x = random.randint(0, self.width-1)
			y = random.randint(0, self.height-1)

			# spawn new food on the board, not on the snake or the current food
			while isinstance(self.board[x][y], Snake) or (x == next_point.x and y == next_point.y):
				x = random.randint(0, self.width-1)
				y = random.randint(0, self.height-1)

			self.food.x = x
			self.food.y = y
			self.snake.eat()
			self.score += 1
		else:
			# set last tail point from Snake to Point type
			tail = self.snake.tail()
			self.board[tail.x][tail.y] = Point(0, 0)

		# move the snake's body (without head)
		self.snake.move_body()

	def move(self, direction):
		# check if snake's new direction is valid
		self.snake.check_direction(direction)
		self.snake.direction = direction

		head = self.snake.head()
		if direction == Direction.UP:
			self.spawn_new_food(self.board[head.x - 1][head.y])
			# update snake head position on the board
			self.board[head.x - 1][head.y] = Snake(0, 0)
			# move head in the direction
			head.x -= 1
			return
		elif direction == Direction.DOWN:
			self.spawn_new_food(self.board[head.x + 1][head.y])
			self.board[head.x + 1][head.y] = Snake(0, 0)
			head.x += 1
			return
		elif direction == Direction.LEFT:
			self.spawn_new_food(self.board[head.x][head.y - 1])
			self.board[head.x][head.y - 1] = Snake(0, 0)
			head.y -= 1
			return
		elif direction == Direction.RIGHT:
			self.spawn_new_food(self.board[head.x][head.y + 1])
			self.board[head.x][head.y + 1] = Snake(0, 0)
			head.y += 1
			return


class DirectionException(Exception):
	pass


if __name__ == '__main__':
	try:
		board = Board(11, 19, Snake(5, 9), Food(6, 12))
		board.draw()
		board.print_score()
		while True:
			mode = input('Input: ')
			if mode in ['w', 's', 'a', 'd']:
				board.move(Direction.key(mode))
				board.draw()
				board.print_score()
			else:
				print('Invalid input!')

	except DirectionException:
		print('Invalid snake direction!')
		pass
	except KeyboardInterrupt:
		print()
		pass


