#!/usr/bin/env python
import fcntl
import os
import tty
import termios

"""Non-blocking stdin reader. (http://ballingt.com/nonblocking-stdin-in-python-3/)"""


class Raw(object):
	def __init__(self, stream):
		self.stream = stream
		self.fd = self.stream.fileno()

	def __enter__(self):
		self.original_stty = termios.tcgetattr(self.stream)
		tty.setcbreak(self.stream)

	def __exit__(self, type, value, traceback):
		termios.tcsetattr(self.stream, termios.TCSANOW, self.original_stty)


class NonBlocking(object):
	def __init__(self, stream):
		self.stream = stream
		self.fd = self.stream.fileno()

	def __enter__(self):
		self.orig_fl = fcntl.fcntl(self.fd, fcntl.F_GETFL)
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl | os.O_NONBLOCK)

	def __exit__(self, *args):
		fcntl.fcntl(self.fd, fcntl.F_SETFL, self.orig_fl)
