#!/usr/bin/env python
from enum import Enum


class Point:
	'''Base class for all points on the board.'''
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def draw(self):
		print('.', end='')


class Food(Point):
	'''Food for the snake.'''
	def __init__(self, x, y):
		Point.__init__(self, x, y)
		
	def draw(self):
		print('X', end='')
		
		
class Snake(Point):
	'''The snake itself.'''
	head
	tail = []
	
	def __init__(self, x, y):
		Point.__init__(self, x, y)
		head = Point(x, y)
		tail = [Point(x, y-1), Point(x, y-2), Point(x, y-3)]

	def draw(self):
		print('O', end='')


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
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					snake = self.board[i][j]
					for tail_point in snake.tail:
						self.board[tail_point.x][tail_point.y] = Snake(0, 0)
				self.board[i][j].draw()
			print()

	def move(self, direction):
		for i in range(self.width):
			for j in range(self.height):
				if isinstance(self.board[i][j], Snake):
					if direction == Direction.UP:
						self.board[i][j] = Point(0,0)
						self.board[i - 1][j] = Snake(0, 0)
						return
					elif direction == Direction.DOWN:
						self.board[i][j] = Point(0,0)
						self.board[i + 1][j] = Snake(0, 0)
						return
					elif direction == Direction.LEFT:
						self.board[i][j] = Point(0,0)
						self.board[i][j - 1] = Snake(0, 0)
						return
					elif direction == Direction.RIGHT:
						self.board[i][j] = Point(0,0)
						self.board[i][j + 1] = Snake(0, 0)
						return
			

if __name__ == '__main__':
	try:
		board = Board(11, 19, Snake(5, 9), Food(7, 14))
		while True:
			board.draw()
			mode=input('Input: ')
			board.move(Direction.key(mode))
		
	except ValueError:
		print("Err")


