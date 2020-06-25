#!/usr/bin/env python3
from device.nbstdin import NonBlocking, Raw
from device.nokia_lcd import NokiaLCD
from common.pillow import Pillow
from common.enum import Direction
from game.snake import Board, Snake, Food
from common.exception import CollisionException

import time
import sys
import argparse


def parse_arguments():
	parser = argparse.ArgumentParser(description='Play the classic Snake game from old Nokia phones on Raspberry Pi.')
	parser.add_argument('-i', '--input', default='stdin', help='Input device', required=False)
	parser.add_argument('-o', '--output', default='stdout', help='Output device', required=False)
	parser.add_argument('-s', '--speed', default='2', help='Game speed', required=False)
	args = parser.parse_args()

	if args.input not in ("stdin", "joystick") or args.output not in ("stdout", "lcd"):
		print("Invalid argument!\nRun with -h argument for help.")
		sys.exit(1)

	if args.input == "joystick":
		print("Not implemented yet!")
		sys.exit(1)

	if not args.speed.isnumeric():
		print("Argument speed must be integer.")
		sys.exit(1)
	elif int(args.speed) >= 11 or int(args.speed) <= 0:
		print("Argument speed must be between 1 and 10.")
		sys.exit(1)

	return args


def output_board(board, output_device, lcd, pillow):
	if output_device == "lcd":
		lcd.display_image(pillow.draw_board(board))
	else:
		board.to_stdout()


def output_game_over(board, output_device, lcd, pillow):
	text = "Game over!\nYour score:\n" + str(board.score)

	if output_device == "lcd":
		lcd.display_image(pillow.draw_text(text))
	else:
		print(text)


def main():
	# initial direction is right
	direction = Direction.RIGHT
	# init board size, snake and food position
	board = Board(11, 20, Snake(10, 8), Food(5, 10))

	# parse command line arguments
	args = parse_arguments()

	# init LCD and Pillow
	lcd = NokiaLCD()
	pillow = Pillow(lcd.width, lcd.height)

	# output the board
	output_board(board, args.output, lcd, pillow)

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
					if time.time() - last_update > (1 / int(args.speed)):
						board.next_turn(direction)
						output_board(board, args.output, lcd, pillow)
						last_update = time.time()

	except CollisionException:
		output_game_over(board, args.output, lcd, pillow)
	except IOError:
		print("I/O not ready.")
	except KeyboardInterrupt:
		pass


# run main method
if __name__ == '__main__':
	main()
