#!/usr/bin/env python
from enum import Enum
from nbstdin import NonBlocking, Raw

import random
import time
import sys


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

	def from_key(self):
		if self == 'w':
			return Direction.UP
		elif self == 's':
			return Direction.DOWN
		elif self == 'a':
			return Direction.LEFT
		elif self == 'd':
			return Direction.RIGHT


class Snake(Point):
	"""The snake - represented by a list of Points."""
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
			self.snake.eat()
			self.score += 1
		else:
			# else set last tail point from Snake to Point type
			tail = self.snake.tail()
			self.board[tail.x][tail.y] = Point(0, 0)


class CollisionException(Exception):
	pass


# TODO implement successful game end
# TODO correct initial snake length

if __name__ == '__main__':
	# turn time in seconds - the time it takes to refresh the board
	turn_time = 0.5
	# initial direction is right
	direction = Direction.RIGHT

	# init board size, snake and food position
	board = Board(11, 19, Snake(5, 9), Food(6, 12))
	board.draw()

	try:
		last_update = time.time()

		with Raw(sys.stdin):
			with NonBlocking(sys.stdin):
				while True:
					# read input key from stdin
					key = sys.stdin.read(1)
					if key in ['w', 's', 'a', 'd']:
						direction = Direction.from_key(key)
					elif key == '\x1b':
						# x1b is ESC - ends the game
						break

					time.sleep(0.05)

					# once in a specified turn_time, move the board and redraw it
					if time.time() - last_update > turn_time:
						board.next_turn(direction)
						board.draw()
						last_update = time.time()

	except CollisionException:
		print('GAME OVER :(')
	except IOError:
		print('I/O not ready.')
	except KeyboardInterrupt:
		pass
