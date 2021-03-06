#!/bin/python

"""
This script writes to a specific terminal to execute commands from another terminal
The logic for this script is from this stack overflow post https://stackoverflow.com/a/20386980
"""

import sys, os
import fcntl, termios
import argparse

def raiseError(errorType, error, exitCode=1):
    print(f'\033[31m[{errorType}]\033[0m: {error}')
    exit(exitCode)

if sys.platform not in ("linux", "linux1", "linux2"):
    raiseError("OSError", "This program only runs on linux")

argumentParser = argparse.ArgumentParser(description="execute a command on 1 terminal from another")
argumentParser.add_argument("terminal", metavar="T", type=int, nargs=1)
argumentParser.add_argument("command",  metavar="C", type=str, nargs="+")
argumentParser.add_argument("-n", "--new-line", action="store_const", const=False, default=True)

args = argumentParser.parse_args()

fd = os.open(f"/dev/pts/{args.terminal[0]}", os.O_RDWR)

cmd = " ".join(args.command)
userId = os.getuid()
if userId != 0: raiseError("PermissionError", "Must be run as root")
#in order to execute as command, each byte must be sent with termios.TIOCSTI
#add the new line to simulate enter
if args.new_line: cmd += "\n"
for char in cmd:
   fcntl.ioctl(fd, termios.TIOCSTI, char)
os.close(fd)
