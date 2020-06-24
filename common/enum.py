#!/usr/bin/env python3
from enum import Enum


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
