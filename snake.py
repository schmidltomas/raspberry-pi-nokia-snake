#!/usr/bin/env python
from enum import Enum


class Point:
	'''Base class for all points on the board with x and y coordinates.'''
	x = 0
	y = 0

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def draw(self, x, y):
		print('.', end='')


class Food(Point):
	'''Food for the snake.'''
	def __init__(self, x, y):
		Point.__init__(self, x, y)
		
	def draw(self, x, y):
		print('X', end='')

		
class Snake(Point):
	'''The snake itself - represented by a head Point and list of tail Points.'''
	tail = [Point]
	head = Point
	
	def __init__(self, x, y):
		Point.__init__(self, x, y)
		self.head = Point(x, y)
		self.tail = [Point(x, y-1), Point(x, y-2), Point(x, y-3)]

	def draw(self):
		print('O', end='')

	def draw(self, x, y):
		if x == self.head.x and y == self.head.y:
			print('O', end='')
		else:
			print('o', end='')


class Direction(Enum):
	'''Direction in which the snake moves.'''
	UP = 1
	DOWN = 2
	LEFT = 3
	RIGHT = 4
	
	def key(key):
		if key == 'w':
			return Direction.UP
		elif key == 's':
			return Direction.DOWN
		elif key == 'a':
			return Direction.LEFT
		elif key == 'd':
			return Direction.RIGHT


class Board():
	'''Playing board.'''
	direction = Direction.RIGHT
	
	def __init__(self, width, height, snake, food):
		self.width = width
		self.height = height
		self.board = [[Point(0, 0) for x in range(self.height)] for y in range(self.width)]
		self.board[snake.x][snake.y] = snake
		self.board[food.x][food.y] = food
	
	def draw(self):
		# find snake head on board
		# TODO to find_head() function
		debug = ""
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					snake = self.board[i][j]
					if i == snake.head.x and j == snake.head.y:
						debug += "snake head at {0},{1}\n".format(i, j)
						# TODO needed?
						# self.board[snake.head.x][snake.head.y] = snake
						# draw snake tail on board
						for tail_point in snake.tail:
							self.board[tail_point.x][tail_point.y] = snake
							debug += "snake tail at {0},{1}\n".format(tail_point.x, tail_point.y)
		print(debug)

		# draw board
		for i in range(self.width):
			for j in range(self.height):
				self.board[i][j].draw(i, j)
				# print(self.board[i][j])
			print()

	# TODO use only x+y or i+j
	def move(self, direction):
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					snake = self.board[i][j]
					if i == snake.head.x and j == snake.head.y:
						# move last element of tail to where head is
						last_tail_point = snake.tail[len(snake.tail)-1]
						last_tail_point.x = snake.head.x
						last_tail_point.y = snake.head.y
						print("last tail point: {0},{1}".format(last_tail_point.x, last_tail_point.y))
						self.board[last_tail_point.x][last_tail_point.y] = Point

						if direction == Direction.UP:
							# move head in the direction
							snake.head.x -= 1
							# update snake head position on the board
							self.board[i - 1][j] = snake
							return
						elif direction == Direction.DOWN:
							snake.head.x += 1
							self.board[i + 1][j] = snake
							return
						elif direction == Direction.LEFT:
							snake.head.y -= 1
							self.board[i][j - 1] = snake
							return
						elif direction == Direction.RIGHT:
							snake.head.y += 1
							self.board[i][j + 1] = snake
							return
			

if __name__ == '__main__':
	try:
		board = Board(11, 19, Snake(5, 9), Food(7, 14))
		board.draw()
		while True:
			mode=input('Input: ')
			board.move(Direction.key(mode))
			board.draw()
		
	except KeyboardInterrupt:
		print()
		pass


