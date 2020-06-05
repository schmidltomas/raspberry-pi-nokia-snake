#!/usr/bin/env python
from enum import Enum


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


class Board():
	"""Playing board."""
	snake = Snake
	food = Food
	
	def __init__(self, width, height, snake, food):
		self.width = width
		self.height = height
		self.board = [[Point(0, 0) for x in range(self.height)] for y in range(self.width)]
		self.snake = snake
		self.food = food
	
	def draw(self):
		# draw snake on board

		for body_point in self.snake.body:
			# TODO redundant setting of Snake instance on all body points?
			self.board[body_point.x][body_point.y] = self.snake

		# draw food
		self.board[self.food.x][self.food.y] = self.food

		# draw board
		for x in range(self.width):
			for y in range(self.height):
				self.board[x][y].draw(x, y)
			print()


	def move(self, direction):
		# check if snake's new direction is valid
		self.snake.check_direction(direction)
		self.snake.direction = direction

		# set last tail point from Snake to Point type
		tail = self.snake.tail()
		self.board[tail.x][tail.y] = Point(0, 0)

		# move the snake's body (without head)
		self.snake.move_body()

		head = self.snake.head()
		if direction == Direction.UP:
			# update snake head position on the board
			self.board[head.x - 1][head.y] = Snake(0, 0)
			# move head in the direction
			head.x -= 1
			return
		elif direction == Direction.DOWN:
			self.board[head.x + 1][head.y] = Snake(0, 0)
			head.x += 1
			return
		elif direction == Direction.LEFT:
			self.board[head.x][head.y - 1] = Snake(0, 0)
			head.y -= 1
			return
		elif direction == Direction.RIGHT:
			self.board[head.x][head.y + 1] = Snake(0, 0)
			head.y += 1
			return


class DirectionException(Exception):
	pass


if __name__ == '__main__':
	try:
		board = Board(11, 19, Snake(5, 9), Food(7, 14))
		board.draw()
		while True:
			mode=input('Input: ')
			if mode in ['w', 's', 'a', 'd']:
				board.move(Direction.key(mode))
				board.draw()
			else:
				print('Invalid input!')

	except DirectionException:
		print('Invalid snake direction!')
		pass
	except KeyboardInterrupt:
		print()
		pass


