#!/usr/bin/python

""""Telekinesis

Usage:
	telekinesis list
	telekinesis info -shard-name SHARD_NAME
	telekinesis -h | --help
	telekinesis -v | --version

Options:
	list		List all Kinesis Streams
	info		Get more info about a particular Kinesis Stream

	-h --help     	Show this screen.
	-v --version	Show version.
"""

import docopt
import commands
from inspect import getmembers, isclass


if __name__ == "__main__":

	try:
		#Parse arguments
		arguments = docopt.docopt(__doc__, version='Telekinesis v0.1')
		print arguments

		for k, v in arguments.iteritems():
			if hasattr(commands, k) and v == True:
				module = getattr(commands, k)
				commands = getmembers(module, isclass)
				command = [command[1] for command in commands if command[0] != 'Base'][0]
				command = command(arguments)
				command.run()

	except docopt.DocoptExit as e:
		print e.message
