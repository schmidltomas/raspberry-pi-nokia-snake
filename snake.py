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

	def key(self, key):
		if key == 'w':
			return Direction.UP
		elif key == 's':
			return Direction.DOWN
		elif key == 'a':
			return Direction.LEFT
		elif key == 'd':
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
	
	def __init__(self, width, height, snake, food):
		self.width = width
		self.height = height
		self.board = [[Point(0, 0) for x in range(self.height)] for y in range(self.width)]
		self.board[snake.x][snake.y] = snake
		self.board[food.x][food.y] = food
	
	def draw(self):
		# find snake head on board
		# TODO to find_head() function, or keep head in a property and get rid of for's in move()?
		# debug = ""
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					snake = self.board[i][j]
					if i == snake.body[0].x and j == snake.body[0].y:
						# debug += "snake head at {0},{1}\n".format(i, j)
						# draw snake body on board
						for body_point in snake.body:
							self.board[body_point.x][body_point.y] = snake
							# debug += "snake body at {0},{1}\n".format(body_point.x, body_point.y)
		# print(debug)

		# draw board
		for i in range(self.width):
			for j in range(self.height):
				self.board[i][j].draw(i, j)
			print()

			
	# TODO use only x+y or i+j?
	def move(self, direction):
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					snake = self.board[i][j]
					if i == snake.body[0].x and j == snake.body[0].y:
						# set last tail point from Snake to Point type
						self.board[snake.tail().x][snake.tail().y] = Point(0, 0)

						# move the snake's tail
						snake.move_body()

						# check if snake's new direction is valid
						snake.check_direction(direction)
						snake.direction = direction

						if direction == Direction.UP:
							# move head in the direction
							snake.body[0].x -= 1
							# update snake head position on the board
							self.board[i - 1][j] = snake
							return
						elif direction == Direction.DOWN:
							snake.body[0].x += 1
							self.board[i + 1][j] = snake
							return
						elif direction == Direction.LEFT:
							snake.body[0].y -= 1
							self.board[i][j - 1] = snake
							return
						elif direction == Direction.RIGHT:
							snake.body[0].y += 1
							self.board[i][j + 1] = snake
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


