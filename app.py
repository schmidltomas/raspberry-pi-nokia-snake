#!/usr/bin/env python
from device.nbstdin import NonBlocking, Raw
from device.nokia_lcd import NokiaLCD
from common.pillow import Pillow
from game.snake import Board, Snake, Food, Direction, CollisionException

import time
import sys
import argparse


def parse_arguments():
	parser = argparse.ArgumentParser(description='Play the classic Snake game from old Nokia phones on Raspberry Pi.')
	parser.add_argument('-i', '--input', default='keyboard', help='Input device', required=False)
	parser.add_argument('-o', '--output', default='lcd', help='Output device', required=False)
	args = parser.parse_args()

	if args.input not in ("stdin", "joystick") or args.output not in ("stdout", "lcd"):
		print("Invalid argument!\nRun with -h argument for help.")
		sys.exit(1)

	return args.input, args.output


if __name__ == '__main__':
	# turn time in seconds - the time it takes to refresh the board
	turn_time = 0.5
	# initial direction is right
	direction = Direction.RIGHT
	# init board size, snake and food position
	board = Board(11, 20, Snake(10, 8), Food(5, 10))

	# parse command line arguments
	input_device, output_device = parse_arguments()
	if input_device == "joystick":
		print("Not implemented yet!")
		sys.exit(1)

	lcd = NokiaLCD()
	pillow = Pillow(lcd.width, lcd.height)

	if output_device == "lcd":
		lcd.display_image(pillow.draw_board(board))
	else:
		board.to_stdout()

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
						last_update = time.time()
						if output_device == "lcd":
							lcd.display_image(pillow.draw_board(board))
						else:
							board.to_stdout()

	except CollisionException:
		text = "Game over!\nYour score:\n" + str(board.score)

		if output_device == "lcd":
			lcd.display_image(pillow.draw_text(text))
		else:
			print(text)

	except IOError:
		print("I/O not ready.")
	except KeyboardInterrupt:
		pass
